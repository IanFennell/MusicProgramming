## Midify

# A Midi modification program for Python for creating backing-tracks

# Requirements
    -fluidsynth
    -python3.7
    -mido

# Usage
    Using python 3.7. Run the Midify_api.py file to boot into the python api.
    Or simply download and run the install script install.sh as sudo to boot straight into the api

    Once in the Python api:
    -load a midi file from the /songs/ directory using the "load [filename]" command.
    -Remove instruments either by range or by a single instrument using the remove [single|range] [instrument number|instrument number] command.
    -Save files to a particular location using the save [location] command
    -Play the worked on midi file by using the play command, Otherwise use play [location] to play a file at a location
    -List the songs in the /songs/ directory using the list command
    -reset the current edited song to default using reset
    -access help by running help [command]
    -exit uisng exit or ctrl-C to force exit
