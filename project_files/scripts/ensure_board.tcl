# Resolve the selected preset inside the Vivado process that builds the overlay.
namespace eval pp4fpga {
    variable board_downloader [file join [file dirname [info script]] fetch_board_files.py]
}

proc pp4fpga::add_board_repo {directory} {
    if {![file isdirectory $directory]} {
        error "Board repository does not exist: $directory"
    }
    set directory [file normalize $directory]
    set repositories [get_param board.repoPaths]
    if {[lsearch -exact $repositories $directory] < 0} {
        set_param board.repoPaths [linsert $repositories 0 $directory]
    }
}

proc pp4fpga::ensure_board {target board_part board_repo board_cache python} {
    variable board_downloader
    if {$board_repo ne ""} {
        add_board_repo $board_repo
    }
    if {[llength [get_board_parts -quiet $board_part]] == 1} {
        puts "Using Vivado board preset: $board_part"
        return
    }
    if {$board_repo ne ""} {
        error "Board '$board_part' was not found in BOARD_REPO '$board_repo' or Vivado's installed presets. Check BOARD_PART and BOARD_REPO."
    }
    puts "Board '$board_part' is missing from Vivado; checking cached board files in $board_cache."
    # Ignore Vivado's PYTHONHOME/PYTHONPATH when using the caller's interpreter.
    if {[catch {exec $python -E $board_downloader --target $target --cache-dir $board_cache} fetched_repo]} {
        error "Could not fetch board files: $fetched_repo"
    }
    add_board_repo [string trim $fetched_repo]
    if {[llength [get_board_parts -quiet $board_part]] != 1} {
        error "Downloaded board files were registered, but preset '$board_part' is unavailable. Check BOARD_PART, or provide custom board files using BOARD_REPO."
    }
    puts "Registered board files: [string trim $fetched_repo]"
    puts "Using Vivado board preset: $board_part"
}
