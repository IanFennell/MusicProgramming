messages={"execution_failed":'''\nExecution failed, please choose from the following options:
remove {range|single} {instrument, name if range, int if single} 
load {song location} 
save {save location}
play [optional location]
reset
exit\n''',
"prompt":"Please enter a command:\n",
"clean_temp":"\nCleaning up /temp Directory\n",
"exit":"\nExiting Now\n",
"save":"Saved!",
"comp_play":"Completed Playing!",
"reset":"Reset",
"ensure_root":"Playing,\nIf there's any issues, Ensure you're running the script as root"
}

format_messages={"invalid_scope":"{} is not a valid option, Valid options are:\n-single\n-range",
        "inst_removed":"{} Removed Successfully",
        "songs":"songs/{}",
        "failed_songs":"Failed to find songs/{}",
        "succ_songs":"{} Loaded Successfully",
        }

error_messages={"unsupp_range":"Please try with the following instruments:",
        "unsupp_single":"Try again with a number 0 < n ≤ 127",
        "unsupp_inst":"That is not a Supported Instrument,\n",
        "failed_find":"{} is not a valid midi file, please choose another"
        }
