import core
import midify_messages
import os
import shutil
from mido import MidiFile
from core import NoInstrumentError, NoSongDirectoryException, InvalidIntError, NotASongLocationException, NoFluidSynthError


def RemoveScopeError(Exception):
    pass

instructions = {"single":core.remove_single_instrument,
                "range":core.remove_instrument_range}



def main():
    # remember to:
    # -clean up code
    # -Set wait to play? Simple os.sleep
    # -Only support for single tracks
    # -Undo Stack, not REALLY required
    # -Add guards to FluidSynth in case it isn't installed
    # -Add user input guards? eg locations
    # -Fairly near done honestly
    if not os.path.exists("./temp"):
        print("Creating /temp directory")
        os.mkdir("temp")
    if not os.path.exists("./songs"):
        raise NoSongDirectoryException
    options = Options()
    messages = midify_messages.messages
    try:
        Original_prompt = messages["prompt"]
        prompt = Original_prompt
        while True:
            commands_in = input(prompt).split(" ")
            commands_in = [row for row in commands_in if row !=""]
            try:
                prompt = f"{getattr(options, commands_in[0])(commands_in[1:])}\n\n{Original_prompt}"
            except AttributeError:
                print(messages["execution_failed"])
    except KeyboardInterrupt:
        print(messages["clean_temp"])
        shutil.rmtree("temp")
        print(messages["exit"])
        exit()

class Options:
    def __init__(self):
        self.midify_messages = midify_messages.messages
        self.form_messages = midify_messages.format_messages
        self.midi_file = MidiFile()
        self.messages = []
        self.original_messages = []

    def remove(self, args):
        if len(args) < 2:
            return self.midify_messages["remove_failed"]
        scope = args[0]
        instrument = args[1]
        try:
            if len(self.messages) == 0:
                return self.midify_messages["empty"]
            self.messages = instructions[scope](instrument, self.messages)
        except KeyError:
            print(self.form_messages["invalid_scope"].format(scope))
            raise RemoveScopeError
        except NoInstrumentError:
            return self.form_messages["failed_remove"].format(instrument)
        except InvalidIntError:
            return self.form_messsages["failed_remove"].format(instrument)
        return self.form_messages["inst_removed"].format(instrument)

    def load(self, args):
        if len(args) == 0:
            return self.midify_messages["load_failed"]
        song_location = args[0]
        if song_location[-4:] != ".mid":
            song_location += ".mid"
        try:
            self.midi_file = MidiFile(self.form_messages["songs"].format(song_location))
            for message in self.midi_file.tracks[0]:
                self.messages.append(message)
            self.original_messages = self.messages
        except FileNotFoundError:
            return self.form_messages["failed_songs"].format(song_location)
        return self.form_messages["succ_songs"].format(song_location)

    def save(self, args):
        if len(args) == 0:
            return self.midify_messages["save_failed"]
        if len(self.messages) == 0:
            return self.midify_messages["empty"]
        location = args[0]
        core.save_messages(self.midi_file, self.messages, location)
        return self.midify_messages["save"]

    def play(self, args):
        if len(args) == 0:
            if len(self.messages) == 0:
                return self.midify_messages["empty"]
            core.save_messages(self.midi_file, self.messages)
            print(self.midify_messages["ensure_root"])
            core.play_song()
            os.remove("temp/output.mid")
        else:
            song_location = args[0]
            if song_location[-4:] != ".mid":
                song_location+=".mid"
            try:
                core.play_song(self.form_messages["songs"].format(song_location))
            except NoFluidSynthError:
                return ""
        return self.midify_messages["comp_play"]
    
    def list(self, args):
        songs_list = os.listdir("./songs")
        midi_list = [row for row in songs_list if row[-4:] == ".mid"]
        if len(midi_list) > 20:
            print(self.midify_messages["long_list"])
            if input().lower() in "no":
                return ""
        for index in range(1, len(midi_list), 2):
            spaces = " "*(80-(len(midi_list[index])+len(midi_list[index-1])))
            print(f"{midi_list[index]}{spaces}{midi_list[index-1]}")
        if len(midi_list) % 2 != 0:
            print(midi_list[-1])
        return ""

    def help(self, args):
        if len(args) == 0:
            return self.midify_messages["empty_help"]
        command_in = args[0]
        help_messages = midify_messages.help_messages
        if command_in not in help_messages.keys():
            command_in = "error"
        return help_messages[command_in]

    def reset(self, args):
        self.messages = self.original_messages
        return messages["reset"]

    def exit(self, args):
        raise KeyboardInterrupt

if __name__ == "__main__":
    main()
