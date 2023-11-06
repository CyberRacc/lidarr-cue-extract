#!/bin/bash

# Function to check if a command exists
command_exists () {
    type "$1" &> /dev/null ;
}

# Dependency check and install function
install_dependencies () {
    if command_exists apt-get ; then
        sudo apt-get install cuetools shntool flac
    elif command_exists yum ; then
        sudo yum install cuetools shntool flac
    elif command_exists pacman ; then
        sudo pacman -S cuetools shntool flac
    else
        echo "Package manager not recognized. Install cuetools, shntool, and flac manually."
        exit 1
    fi
}

# Check for dependencies and install if not present
if ! command_exists cuebreakpoints || ! command_exists shnsplit ; then
    echo "Required tools not found. Installing..."
    install_dependencies
fi

# Script usage
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 file.cue file.flac"
    exit 1
fi

# Variables for files
CUE_FILE="$1"
FLAC_FILE="$2"

# Split FLAC file according to CUE sheet
cuebreakpoints "$CUE_FILE" | shnsplit -o flac "$FLAC_FILE"

# Apply tags from CUE sheet to split files
cuetag "$CUE_FILE" split-track*.flac

echo "Splitting complete. Tracks have been output with metadata."
