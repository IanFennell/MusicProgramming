from mido import MidiFile, MidiTrack, Message
import midify_messages
import os
import sys
import subprocess

class NoSongDirectoryException(Exception):
    pass

class NotASongLocationException(Exception):
    pass

class NoInstrumentError(Exception):
    pass

class InvalidIntError(Exception):
    pass

class NoFluidSynthError(Exception):
    pass

errors = midify_messages.error_messages

def remove_instrument_range(instrument, messages):
    global errors
    global instrument_ranges
    if instrument not in instrument_ranges:
        print(f"{errors['unsupp_inst']}{errors[unsupp_range]}")
        for instrument in instrument_ranges.keys():
            print(f"-{instrument}")
        raise NoInstrumentError
    return remove_instrument(instrument, messages, equal_range)

def remove_single_instrument(instrument_num, messages):
    try:
        instrument_num = int(instrument_num)
    except ValueError:
        print("Please enter a valid Number")
        raise InvalidIntError
    if instrument_num not in range(1,128):
        print(f"{errors['unsupp_inst']}{errors['unsupp_single']}")
        raise NoInstrumentError
    return remove_instrument(instrument_num, messages, equal_single)

def equal_single(prog, instrument):
    return prog == instrument

def equal_range(prog, instrument):
    global instrument_ranges
    return prog in instrument_ranges[instrument]

def remove_instrument(instrument, messages, equal_function):
    ret_messages = []
    channels_to_be_removed = []
    for message in messages:
        if "channel=" in str(message):
            chan = get_property("channel", str(message))
            if "program_change" in str(message):
                prog = get_property("program",str(message))
                if equal_function(prog, instrument):
                    channels_to_be_removed.append(chan)
                ret_messages.append(message)
            elif chan in channels_to_be_removed and "note_on" in str(message):
                ret_messages.append(Message("note_on", channel=chan, velocity=0, time=get_property("time",str(message))))
            else:
                ret_messages.append(message)
        else:
            ret_messages.append(message)
    return ret_messages

def get_property(prop, message):
    index = message.index(f"{prop}=")+ (len(prop)+1)
    try:
        ret_int = int(message[index:index+3])
    except ValueError:
        ret_int = int(message[index:index+2])
    return ret_int

def save_messages(mido_file, messages, location="temp/output.mid"):
    mido_file.tracks[0] = messages
    mido_file.save(location)

def play_song(location="temp/output.mid", quiet=True):
    global errors
    if not os.path.exists(location):
        print(errors["failed_find"].format(location))
    else:
        run_args = ["fluidsynth", "-a", "alsa", "-m", "alsa_seq", "-l", "-i", "Soundfont.sf2", location]
        if quiet:
            output = open(os.devnull, "w")
        else:
            output = sys.stdout
        try:
            subprocess.call(run_args, stdout=output, stderr=output)
        except FileNotFoundError:
            print(errors["failed_fluidsynth"])
            raise NoFluidSynthError
        
instrument_ranges = {"piano": range(1,9),
                     "Chromatic Percussion":range(9,17),
                     "Organ": range(17,25),
                     "guitar":range(25,33),
                     "Bass": range(30,41),
                     "Orchestra Solo": range(41,49),
                     "Orchestra Ensemble": range(49,57),
                     "Brass": range(57,65),
                     "Reed": range(65,73),
                     "Wind": range(73,81),
                     "Synth Lead": range(81,89),
                     "Synth Pad": range(89,97),
                     "Synth Sound FX": range(97,105),
                     "Ethnic": range(105,113),
                     "Percusssive": range(113,121),
                     "Misc SFX": range(121,129),
                     }

