#!/bin/bash

cleanup() {
    # Make sure Fenrir is restored on exit of this script
    echo -n "setting set screen#suspendingScreen=" | socat - UNIX-CLIENT:/tmp/fenrirscreenreader-deamon.sock
}

# Call the cleanup function on exit of this script
trap cleanup EXIT

# Get the number of the current terminal
term=$(tty)
term="${term##*tty}"

# Make sure term is a number, otherwise we're in something like screen, and x will not start.
if ! [[ "$term" =~ ^[1-9]+$ ]]; then
    echo "This does not appear to be a terminal from where X may be started. Please make sure you are not in a screen or tmux session."
    trap - EXIT
    exit 1
fi

# Suspend the current terminal for Fenrir
echo -n "setting set screen#suspendingScreen=$term" | socat - UNIX-CLIENT:/tmp/fenrirscreenreader-deamon.sock

# Start the x session
command startx

exit 0
