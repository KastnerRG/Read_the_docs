#!/bin/sh
# Usage: run_checked.sh OUTPUT LABEL COMMAND [ARGS...]
# vitis-run and vivado can exit 0 when they fail to start, so run COMMAND and
# fail unless it wrote a new OUTPUT. A previous OUTPUT is set aside and put
# back if no new one appears, so a failed rebuild never loses a working result.
output=$1
label=$2
shift 2

restore() {
    if [ ! -e "$output" ] && [ -e "$output.prev" ]; then
        mv -f "$output.prev" "$output"
        restored=1
    else
        rm -f "$output.prev"
    fi
}

restored=
trap 'restore; exit 130' INT TERM
if [ -e "$output" ]; then mv -f "$output" "$output.prev"; fi
"$@"
status=$?
trap - INT TERM
restore
if [ "$status" -ne 0 ]; then exit "$status"; fi
if [ -n "$restored" ] || [ ! -e "$output" ]; then
    echo "error: $label did not produce $output; see the tool output above." >&2
    if [ -n "$restored" ]; then echo "The previous $output was left in place." >&2; fi
    echo 'On ieng6, "libtinfo.so.5" errors mean the LD_LIBRARY_PATH setup from docs/PYNQ-example.rst is missing.' >&2
    exit 1
fi
