"""Test board discovery and cached downloads without AMD tools or network access."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

try:
    import tkinter
except ImportError:
    tkinter = None


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import fetch_board_files as boards


@unittest.skipUnless(shutil.which("git"), "Git is required for local checkout tests")
class BoardDownloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.upstream = self.directory / "upstream"
        self.upstream.mkdir()
        definitions = [
            "board-files/aup-zu3-4gb/1.0/board.xml",
            "board-files/aup-zu3-8gb/1.0/board.xml",
            "boards/TUL/pynq-z2/A.0/board.xml",
            "unrelated/board.xml",
        ]
        for filename in definitions:
            path = self.upstream / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("<board/>\n")
        for args in [
            ["init", "-q"], ["add", "."],
            ["-c", "user.name=Board tests", "-c", "user.email=board-tests@example.invalid",
             "commit", "-qm", "Local board fixtures"],
        ]:
            subprocess.run(["git", *args], cwd=self.upstream, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sources = {target: {**source, "url": self.upstream.as_uri()}
                   for target, source in boards.BOARD_SOURCES.items()}
        patcher = mock.patch.dict(boards.BOARD_SOURCES, sources)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.cache = self.directory / "board files"

    def test_both_boards_are_downloaded_sparsely_and_reused_offline(self):
        for target in ("zu3", "pynq"):
            with self.subTest(target=target):
                board_root = boards.fetch_board_files(target, self.cache)
                self.assertTrue(boards.has_board_files(board_root))
                checkout = self.cache / boards.BOARD_SOURCES[target]["name"]
                self.assertTrue((checkout / ".git").is_dir())
                self.assertFalse((checkout / "unrelated").exists())
                with mock.patch.object(boards, "run_git", side_effect=AssertionError("Offline cache must not run Git")):
                    self.assertEqual(boards.fetch_board_files(target, self.cache), board_root)

    def test_failed_clone_leaves_no_partial_checkout_and_can_be_retried(self):
        with mock.patch.dict(boards.BOARD_SOURCES["zu3"], {"url": (self.directory / "missing").as_uri()}):
            with self.assertRaises(RuntimeError):
                boards.fetch_board_files("zu3", self.cache)
        self.assertEqual(list(self.cache.iterdir()), [])
        self.assertTrue(boards.has_board_files(boards.fetch_board_files("zu3", self.cache)))

    def test_unrecognized_existing_cache_is_preserved(self):
        checkout = self.cache / boards.BOARD_SOURCES["zu3"]["name"]
        checkout.mkdir(parents=True)
        marker = checkout / "keep.txt"
        marker.write_text("Keep existing user files\n")
        with self.assertRaisesRegex(RuntimeError, "contains no board definitions"):
            boards.fetch_board_files("zu3", self.cache)
        self.assertEqual(marker.read_text(), "Keep existing user files\n")

    def test_git_uses_the_callers_libraries_and_preserves_the_parent_environment(self):
        paths = {"LD_LIBRARY_PATH": "/vivado/libraries", "PP4FPGA_HOST_LD_LIBRARY_PATH": "/caller/libraries"}
        with mock.patch.dict(os.environ, paths), mock.patch.object(boards.subprocess, "run") as run:
            boards.run_git("--version")
            self.assertEqual(run.call_args.kwargs["env"]["LD_LIBRARY_PATH"], "/caller/libraries")
            self.assertEqual(os.environ["LD_LIBRARY_PATH"], "/vivado/libraries")

    def test_standalone_download_preserves_the_callers_libraries(self):
        with mock.patch.dict(os.environ, {"LD_LIBRARY_PATH": "/caller/libraries"}, clear=True):
            with mock.patch.object(boards.subprocess, "run") as run:
                boards.run_git("--version")
                self.assertEqual(run.call_args.kwargs["env"]["LD_LIBRARY_PATH"], "/caller/libraries")

    def test_downloader_runs_when_vivado_sets_a_different_pythonhome(self):
        environment = os.environ.copy()
        environment["PYTHONHOME"] = "/vivado/bundled/python"
        code = (
            "import sys\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "import fetch_board_files as boards\n"
            "boards.BOARD_SOURCES['zu3']['url'] = sys.argv[2]\n"
            "print(boards.fetch_board_files('zu3', sys.argv[3]))\n"
        )
        result = subprocess.run([sys.executable, "-E", "-c", code, str(SCRIPTS),
                                 self.upstream.as_uri(), str(self.cache)], env=environment,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(boards.has_board_files(Path(result.stdout.strip())))


@unittest.skipIf(tkinter is None, "Python's Tcl interpreter is required")
class VivadoBoardDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.board_root = self.directory / "downloaded board files"
        self.board_root.mkdir()
        self.interp = tkinter.Tcl()
        self.interp.eval("""
            set test_repositories {/existing/boards}
            set test_available 0
            set test_downloads 0
            proc get_param {name} { return $::test_repositories }
            proc set_param {name value} { set ::test_repositories $value }
            proc get_board_parts {args} {
                if {$::test_available || [lsearch -exact $::test_repositories $::test_expected_repo] >= 0} {
                    return [list [lindex $args end]]
                }
                return {}
            }
            proc exec {args} {
                incr ::test_downloads
                set ::test_download_args $args
                return $::test_downloaded_repo
            }
        """)
        self.interp.setvar("test_expected_repo", str(self.board_root))
        self.interp.setvar("test_downloaded_repo", str(self.board_root) + "\n")
        self.interp.call("source", str(SCRIPTS / "ensure_board.tcl"))

    def ensure_board(self, board_repo=""):
        self.interp.call("pp4fpga::ensure_board", "zu3",
                         "realdigital.org:aup-zu3-4gb:part0:1.0", board_repo,
                         str(self.directory / "cache"), sys.executable)

    def test_installed_preset_never_downloads(self):
        self.interp.setvar("test_available", 1)
        self.ensure_board()
        self.assertEqual(int(self.interp.getvar("test_downloads")), 0)
        self.assertFalse((self.directory / "cache").exists())

    def test_missing_preset_is_registered_and_existing_paths_are_preserved(self):
        self.ensure_board()
        self.assertEqual(int(self.interp.getvar("test_downloads")), 1)
        download_args = self.interp.splitlist(self.interp.getvar("test_download_args"))
        self.assertEqual(download_args[:2], (sys.executable, "-E"))
        repositories = tuple(map(str, self.interp.splitlist(self.interp.getvar("test_repositories"))))
        self.assertEqual(repositories, (str(self.board_root), "/existing/boards"))
        self.ensure_board()
        self.assertEqual(int(self.interp.getvar("test_downloads")), 1)

    def test_explicit_repo_is_used_without_download(self):
        self.ensure_board(str(self.board_root))
        self.assertEqual(int(self.interp.getvar("test_downloads")), 0)

    def test_invalid_explicit_repo_reports_missing_preset_without_download(self):
        self.interp.setvar("test_expected_repo", "/another/board/repository")
        with self.assertRaisesRegex(tkinter.TclError, "was not found in BOARD_REPO"):
            self.ensure_board(str(self.board_root))
        self.assertEqual(int(self.interp.getvar("test_downloads")), 0)


if __name__ == "__main__":
    unittest.main()
