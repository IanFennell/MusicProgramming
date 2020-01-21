import core
import midify_messages
import os
import shutil
from mido import MidiFile

def RemoveScopeError(Exception):
    pass

instructions = {"single":core.remove_single_instrument,
                "range":core.remove_instrument_range}

def main():
    # remember to:
    # -clean up code
    # -Set wait to play? Simple os.sleep
    # -Name it?
    # -Only support for single tracks
    # -Undo Stack, not REALLY required
    # -Fairly near done honestly
    options = Options()
    messages = midify_messages.messages
    try:
        Original_prompt = "Please enter a command:\n"
        prompt = Original_prompt
        while True:
            commands_in = input(prompt).split(" ")
            commands_in = [row for row in commands_in if row !=""]
            try:
                print(commands_in)
                prompt = f"{getattr(options, commands_in[0])(commands_in[1:])}\n{Original_prompt}"

            except AttributeError:
                print(messages["execution_failed"])
    except KeyboardInterrupt:
        print("Cleaning up /temp directory")
        shutil.rmtree("temp")
        print("Exiting now")
        exit()

class Options:
    def __init__(self):
        self.midi_file = MidiFile()
        self.messages = []
        self.original_messages = []

    def remove(self, args):
        scope = args[0]
        instrument = args[1]
        try:
            print(instructions[scope])
            self.messages = instructions[scope](instrument, self.messages)
        except KeyError:
            print(f"{scope} is not a valid option, Valid options are:\n-single\n-range")
            raise RemoveScopeError
        return f"{instrument} Removed Successfully"

    def load(self, args):
        song_location = args[0]
        if song_location[-4:] != ".mid":
            song_location += ".mid"
        try:
            self.midi_file = MidiFile(f"songs/{song_location}")
            for message in self.midi_file.tracks[0]:
                self.messages.append(message)
            self.original_messages = self.messages
        except FileNotFoundError:
            return f"Failed to find songs/{song_location}"
        return f"{song_location} Loaded Successfully"

    def save(self, args):
        location = args[0]
        core.save_messages(self.midi_file, self.messages, location)
        return "Saved!"

    def play(self, args):
        if len(args) == 0:
            core.save_messages(self.midi_file, self.messages)
            print("Playing, if there's any issues, Ensure you're playing the script as root")
            core.play_song()
            os.remove("temp/output.mid")
        else:
            try:
                song_location = args[0]
                if song_location[-4:] != ".mid":
                    song_location+=".mid"
                core.play_song(f"songs/{song_location}")
            except NotASongLocationException:
                print(f"{location} is not a valid midi file, please choose another")
        return "Completed Playing"

    def reset(self, args):
        self.messages = self.original_messages
        return "Reset"

    def exit(self, args):
        raise KeyboardInterrupt

if __name__ == "__main__":
    if not os.path.exists("./temp"):
        print("Creating /temp directory")
        os.mkdir("temp")
    if not os.path.exists("./songs"):
        raise NoSongDirectoryException
    main()
