"""Board build regressions; run with python3 -m unittest discover -s this directory."""

import configparser
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]
PROJECTS = SCRIPTS.parent
PARTS = {"pynq": "xc7z020clg400-1", "zu3": "xczu3eg-sfvc784-2-e"}


class BoardBuildTests(unittest.TestCase):
    def run_command(self, args, directory):
        result = subprocess.run(args, cwd=directory, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("overriding recipe", result.stderr)
        return result.stdout

    def make(self, directory, *args):
        # Tool discovery needs no installed AMD tools for these regression tests.
        return self.run_command([
            "make", "--no-print-directory", f"PYTHON={sys.executable}",
            "VITIS_HLS_PATH=/tmp/board-test-tools/vitis_hls", *args,
        ], directory)

    def test_every_project_routes_both_boards(self):
        for makefile in sorted(PROJECTS.rglob("Makefile")):
            text = makefile.read_text()
            if "GEN_TCL" not in text:
                continue
            top = re.search(r"^TOP = (\w+)", text, re.MULTILINE).group(1)
            for target, part in PARTS.items():
                with self.subTest(project=makefile.parent, target=target):
                    output = self.make(makefile.parent, "-n", "bitstream", f"TARGET={target}")
                    self.assertIn(part, output)
                    self.assertIn(f"build/{target}", output)
                    component = f"{top}.comp" if target == "pynq" else f"{top}_zu3.comp"
                    self.assertIn(f"{component}/hls/impl/ip", output)

    def test_generator_preserves_config_and_directives_with_part_override(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / "kernel.cpp").touch()
            config = directory / "__hls_config__.ini"
            config.write_text(
                "[DEFAULTS]\npart = configured-part\nperiod = 7\n\n"
                "[kernel.cpp]\ntop = accelerator\nfiles = kernel.cpp helper.cpp\n"
                "tb_files = test.cpp input.dat\ndirectives = directives.tcl\n"
            )
            for part in (None, PARTS["zu3"]):
                args = [sys.executable, str(SCRIPTS / "gen_hls_runner_script.py"),
                        "-i", "kernel.cpp", "-o", "generated.tcl", "--component", "board.comp"]
                if part:
                    args += ["--part", part]
                self.run_command(args, directory)
                script = (directory / "generated.tcl").read_text()
                self.assertIn(f"set_part {part or 'configured-part'}", script)
                self.assertIn("set_top accelerator", script)
                self.assertIn("add_files [list kernel.cpp helper.cpp]", script)
                self.assertIn("add_files -tb [list test.cpp input.dat]", script)
                self.assertLess(script.index("source directives.tcl"), script.index("csynth_design"))
                self.assertIn("create_clock -period 7", script)
            parsed = configparser.ConfigParser()
            parsed.read(config)
            self.assertEqual(parsed["DEFAULTS"]["part"], "configured-part")

    def test_switching_targets_reuses_only_the_matching_component(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            for filename in ("Makefile", "__hls_config__.ini", "mul.cpp", "mul.h", "mul_test.cpp"):
                shutil.copy(PROJECTS / "lab1" / filename, directory)
            fake_hls = directory / "fake_hls.py"
            fake_hls.write_text(
                "from pathlib import Path\nimport re, sys\n"
                "script = Path(sys.argv[1]).read_text()\n"
                "component = re.search(r'open_component (\\S+)', script).group(1)\n"
                "Path(component).mkdir(exist_ok=True)\n"
                "with open('build_calls', 'a') as calls: calls.write(component + '\\n')\n"
            )
            args = [f"GEN_TCL={SCRIPTS / 'gen_hls_runner_script.py'}",
                    f"HLS_COMPILER={sys.executable} {fake_hls}", "hls"]
            self.make(directory, *args)  # The default must still build PYNQ-Z2.
            self.make(directory, *args, "TARGET=zu3")
            self.make(directory, *args, "TARGET=pynq")
            self.assertEqual((directory / "build_calls").read_text().splitlines(),
                             ["mul.comp", "mul_zu3.comp"])
            self.assertIn(PARTS["pynq"], (directory / "mul.tcl").read_text())
            self.assertIn(PARTS["zu3"], (directory / "mul_zu3.tcl").read_text())
            os.utime(directory / "mul.h", None)
            self.make(directory, *args, "TARGET=zu3")
            self.assertEqual((directory / "build_calls").read_text().splitlines()[-1], "mul_zu3.comp")
            self.assertEqual(len((directory / "build_calls").read_text().splitlines()), 3)

    def test_unknown_target_is_rejected(self):
        result = subprocess.run([
            "make", "-n", "hls", "TARGET=unknown", "VITIS_HLS_PATH=/tmp/vitis_hls",
        ], cwd=PROJECTS / "lab1", capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported TARGET", result.stderr)

    def test_failed_synthesis_is_retried(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            for filename in ("Makefile", "__hls_config__.ini", "mul.cpp", "mul.h", "mul_test.cpp"):
                shutil.copy(PROJECTS / "lab1" / filename, directory)
            args = ["make", "--no-print-directory", "VITIS_HLS_PATH=/tmp/vitis_hls",
                    f"GEN_TCL={SCRIPTS / 'gen_hls_runner_script.py'}", f"PYTHON={sys.executable}",
                    "TARGET=zu3", "hls"]
            failed_hls = directory / "fail.py"
            failed_hls.write_text("from pathlib import Path\nPath('mul_zu3.comp').mkdir()\nraise SystemExit(1)\n")
            result = subprocess.run([*args, f"HLS_COMPILER={sys.executable} {failed_hls}"],
                                    cwd=directory, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((directory / "mul_zu3.comp/.csynth").exists())
            output = self.run_command([*args, "HLS_COMPILER=echo SYNTHESIS_RETRIED"], directory)
            self.assertIn("SYNTHESIS_RETRIED mul_zu3.tcl", output)
            self.assertTrue((directory / "mul_zu3.comp/.csynth").exists())


    def test_axi_burst_uses_32_bit_addresses_only_on_pynq(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source = PROJECTS / "lab_axi_burst/axi4_burst"
            for filename in ("Makefile", "__hls_config__.ini", "axi4_sqrt.cpp", "axi4_sqrt_test.cpp"):
                shutil.copy(source / filename, directory)
            for target, suffix in (("pynq", ""), ("zu3", "_zu3")):
                script = f"axi4_sqrt{suffix}.tcl"
                self.make(directory, script, f"TARGET={target}",
                          f"GEN_TCL={SCRIPTS / 'gen_hls_runner_script.py'}")
                text = (directory / script).read_text()
                command = "config_interface -m_axi_addr64=false"
                self.assertEqual(command in text, target == "pynq")
                if target == "pynq":
                    self.assertLess(text.index(command), text.index("csynth_design"))

    def test_clean_preserves_course_sources_and_the_other_board(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            shutil.copy(PROJECTS / "lab1/Makefile", directory)
            keep = ["script.tcl", "directives.tcl", "custom_design.tcl", "mul.comp/.csynth",
                    "mul.tcl", "build/pynq/mul.bit"]
            remove = ["mul_zu3.comp/.csynth", "mul_zu3.tcl", "export_mul_zu3.tcl",
                      "build/zu3/mul.bit", "mul_test.bin"]
            for filename in keep + remove:
                path = directory / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture\n")
            self.make(directory, "clean", "TARGET=zu3",
                      f"GEN_TCL={SCRIPTS / 'gen_hls_runner_script.py'}")
            for filename in keep:
                self.assertTrue((directory / filename).is_file(), filename)
            for filename in remove:
                self.assertFalse((directory / filename).exists(), filename)

    def test_vitis_run_can_supply_the_hls_include_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            tools = directory / "Vitis/bin"
            tools.mkdir(parents=True)
            launcher = tools / "vitis-run"
            launcher.touch(mode=0o755)
            (directory / "Makefile").write_text(
                f"TOP = kernel\nGEN_TCL = {SCRIPTS / 'gen_hls_runner_script.py'}\n"
                f"include {SCRIPTS / 'boards.mk'}\n"
                "print-include:\n\t@printf '%s\\n' '$(VHLS)/include'\n"
            )
            environment = os.environ.copy()
            paths = [path for path in environment["PATH"].split(os.pathsep) if "Xilinx" not in path]
            environment["PATH"] = os.pathsep.join([str(tools), *paths])
            result = subprocess.run(["make", "--no-print-directory", "print-include"],
                                    cwd=directory, env=environment, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), str(directory / "Vitis/include"))

    def test_missing_synthesis_report_is_an_error(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / "kernel.cpp").touch()
            (directory / "__hls_config__.ini").write_text(
                "[DEFAULTS]\npart = configured-part\nperiod = 10\n"
                "[kernel.cpp]\ntop = kernel\ntb_files = none\n"
            )
            (directory / "Makefile").write_text(
                f"TOP = kernel\nGEN_TCL = {SCRIPTS / 'gen_hls_runner_script.py'}\n"
                f"include {SCRIPTS / 'boards.mk'}\n"
            )
            (directory / "kernel.comp").mkdir()
            result = subprocess.run([
                "make", "report", f"PYTHON={sys.executable}", "HLS_COMPILER=true",
            ], cwd=directory, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("kernel_csynth.rpt", result.stderr)

    def test_legacy_make_commands_work_without_target(self):
        for makefile in sorted(PROJECTS.rglob("Makefile")):
            text = makefile.read_text()
            if "GEN_TCL" not in text:
                continue
            top = re.search(r"^TOP = (\w+)", text, re.MULTILINE).group(1)
            for target in (None, "test", "hls", "report", "ip", "clean"):
                with self.subTest(project=makefile.parent, command=target or "make"):
                    args = ["-B", "-n"]
                    if target:
                        args.append(target)
                    output = self.make(makefile.parent, *args)
                    self.assertNotIn(f"{top}_zu3.comp", output)
                    if target not in ("test", "clean"):
                        self.assertIn(PARTS["pynq"], output)
                        self.assertIn(f"--component {top}.comp", output)
                    if target == "report":
                        self.assertIn(f"{top}.comp/hls/syn/report/{top}_csynth.rpt", output)
                    if target == "ip":
                        self.assertIn(f"export_{top}.tcl", output)

    def test_project_configs_reference_existing_sources_and_testbenches(self):
        sys.path.insert(0, str(SCRIPTS))
        from gen_hls_runner_script import get_script_parameters
        for makefile in sorted(PROJECTS.rglob("Makefile")):
            text = makefile.read_text()
            if "GEN_TCL" not in text:
                continue
            top = re.search(r"^TOP = (\w+)", text, re.MULTILINE).group(1)
            match = re.search(r"^HLS_INPUT = (.+)", text, re.MULTILINE)
            input_file = match.group(1) if match else f"{top}.cpp"
            config = configparser.ConfigParser()
            config.read(makefile.parent / "__hls_config__.ini")
            parameters = get_script_parameters(input_file, config)
            with self.subTest(project=makefile.parent):
                self.assertEqual(parameters["top"], top)
                for key in ("files", "tb_files", "directives"):
                    for filename in parameters[key].split():
                        if filename not in ("none", "{}"):
                            self.assertTrue((makefile.parent / filename).is_file(), filename)

    def test_fir128_software_failure_prevents_synthesis(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            for filename in ("Makefile", "__hls_config__.ini", "fir.cpp", "fir_test.cpp"):
                shutil.copy(PROJECTS / "project1/fir128" / filename, directory)
            fake_hls = directory / "fake_hls.py"
            fake_hls.write_text("from pathlib import Path\nPath('synthesis_started').touch()\n")
            result = subprocess.run([
                "make", "hls", f"PYTHON={sys.executable}", "CXX=false",
                f"GEN_TCL={SCRIPTS / 'gen_hls_runner_script.py'}",
                f"HLS_COMPILER={sys.executable} {fake_hls}",
            ], cwd=directory, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((directory / "synthesis_started").exists())


if __name__ == "__main__":
    unittest.main()
