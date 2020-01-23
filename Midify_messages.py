messages={"execution_failed":'''\nExecution failed, please choose from the following options:
remove {range|single} {instrument, name if range, int if single} 
load {song location} 
save {save location}
play [optional location]
list
reset
exit\n''',
"prompt":"Please enter a command:\n",
"clean_temp":"\nCleaning up /temp Directory\n",
"exit":"\nExiting Now\n",
"save":"Saved!",
"comp_play":"Completed Playing!",
"reset":"Reset",
"ensure_root":"Playing,\nIf there's any issues, Ensure you're running the script as root",
"remove_failed":"Failed to remove, please ensure the command is in the form remove [single/range][instrument]",
"empty":"Messages are empty, Either the file has not yet been loaded or the midi messages have been fully removed, please load a file to continue",
"load_failed":"Load Failed, please ensure a location is provided in the form of load [location]",
"save_failed":"Save Failed, please ensure a location to save the midi file to is provided in the form of save [location]",
"long_list":"The songs list is longer than 20 and may clutter the screen, are you sure you wish to continue?",
"empty_help":'''Please choose from the following options:
remove {range|single} {instrument, name if range, int if single} 
load {song location} 
save {save location}
play [optional location]
list
reset
exit\n''',
"on_start":'''
 ___ ___  ____  ___    ____  _____  __ __ 
|   |   ||    ||    \ |    ||     ||  |  |
| _   _ | |  | |     \ |  | |   __||  |  |
|  \_/  | |  | |  |  | |  | |  |_  |  |  |
|   |   | |  | |  |  | |  | |   _] |___  |
|   |   | |  | |     | |  | |  |   |     |
|___|___||____||_____||____||__|   |____/ 
                                          '''
}

format_messages={"invalid_scope":"{} is not a valid option, Valid options are:\n-single\n-range",
        "inst_removed":"{} Removed Successfully",
        "songs":"songs/{}",
        "failed_songs":"Failed to find songs/{}",
        "succ_songs":"{} Loaded Successfully",
        "failed_remove":"Failed to remove {}"
        }
help_messages={"remove":"Remove a particular instrument,\nInput a string 'range' or 'single' followed by a string instrument range,in the case of ranges, or an integer in the range of 1 -> 127.\nRange will remove the instrument entirely, and single will remove one particular instrument from the range.\nThis instrument number and range list can be found on the wikipedia page for the General Midi Spec 2",
        "load":"Load a particular midi file from the /songs/ directory which will be set as the current worked on song.\nTakes in a string which is the song name within the directory",
        "save":"Saves the currently worked on song as a midi file to a particular location input by the user",
        "play":"Plays a Midi song using the FluidSynth midi playing engine.\nCan take in an optional location of a midi file to play.\nIf not given this location, It will save a copy of the current worked on song to the temp directory and play that.",
        "list":"Lists all the midi songs in the /songs/ directory",
        "help":"Displays the help message for any song",
        "reset":"Resets the current worked on song to it's original form",
        "exit":"Cleans up and exits the program",
        "error":"Error, this is not a recognised command.\nPlease try with the following:\n-remove\n-load\n-save\n-play\n-list\n-help\n-reset\n-exit"
        }
error_messages={"unsupp_range":"Please try with the following instruments:",
        "unsupp_single":"Try again with a number 0 < n ≤ 127",
        "unsupp_inst":"That is not a Supported Instrument,\n",
        "failed_find":"{} is not a valid midi file, please choose another",
        "failed_fluidsynth":"Error calling fluidsynth, Please ensure it is installed"
        }
