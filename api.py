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
    # -Midify
    # -Only support for single tracks
    # -Undo Stack, not REALLY required
    # -Fairly near done honestly
    options = Options()
    messages = midify_messages.messages
    form_messages = midify_messages.format_messages
    try:
        Original_prompt = messages["prompt"]
        prompt = Original_prompt
        while True:
            commands_in = input(prompt).split(" ")
            commands_in = [row for row in commands_in if row !=""]
            try:
                print(commands_in)
                prompt = f"{getattr(options, commands_in[0])(commands_in[1:])}\n\n{Original_prompt}\n"

            except AttributeError:
                print(messages["execution_failed"])
    except KeyboardInterrupt:
        print(messages["clean_temp"])
        shutil.rmtree("temp")
        print(messages["exit"])
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
            print(form_messages["invalid_scope"].format(scope))
            raise RemoveScopeError
        return form_messages["inst_removed"].format(instrument)

    def load(self, args):
        song_location = args[0]
        if song_location[-4:] != ".mid":
            song_location += ".mid"
        try:
            self.midi_file = MidiFile(form_messages["songs"].format(song_location))
            for message in self.midi_file.tracks[0]:
                self.messages.append(message)
            self.original_messages = self.messages
        except FileNotFoundError:
            return form_messages["failed_songs"].format(song_location)
        return form_messages["succ_songs"].format(song_location)

    def save(self, args):
        location = args[0]
        core.save_messages(self.midi_file, self.messages, location)
        return messages["save"]

    def play(self, args):
        if len(args) == 0:
            core.save_messages(self.midi_file, self.messages)
            print(messages["ensure_root"])
            core.play_song()
            os.remove("temp/output.mid")
        else:
            song_location = args[0]
            if song_location[-4:] != ".mid":
                song_location+=".mid"
            core.play_song(form_messages["songs"].format(song_location))
        return messages["comp_play"]

    def reset(self, args):
        self.messages = self.original_messages
        return messages["reset"]

    def exit(self, args):
        raise KeyboardInterrupt

if __name__ == "__main__":
    if not os.path.exists("./temp"):
        print("Creating /temp directory")
        os.mkdir("temp")
    if not os.path.exists("./songs"):
        raise NoSongDirectoryException
    main()
