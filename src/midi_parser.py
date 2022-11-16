#!/usr/bin/python
# This class handles the parsing of a midi file and builds a markov
# chain from it.

import hashlib
import mido
import argparse

from markov_chain import MarkovChain, Note, ORDER

class Parser:

    def __init__(self, filename, verbose=False):
        """
        This is the constructor for a Serializer, which will serialize
        a midi given the filename and generate a markov chain of the
        notes in the midi.
        """
        self.filename = filename
        # The tempo is number representing the number of microseconds
        # per beat.
        self.tempo = None
        # The delta time between each midi message is a number that
        # is a number of ticks, which we can convert to beats using
        # ticks_per_beat.
        self.ticks_per_beat = None
        self.markov_chain = MarkovChain()
        self._parse(verbose=verbose)

    def _parse(self, verbose=False):
        """
        This function handles the reading of the midi and chunks the
        notes into sequenced "chords", which are inserted into the
        markov chain.
        """
        midi = mido.MidiFile(self.filename)
        self.ticks_per_beat = midi.ticks_per_beat
        notes_sequence = []
        note_start_time = {}
        time = 0
        # Assume it is monophonic
        for track in midi.tracks:
            for message in track:
                if verbose:
                    print(message)
                if message.type == "set_tempo":
                    self.tempo = message.tempo
                if message.type == "note_on" or message.type == "note_off":
                    time += message.time
                    # If the note is off
                    if message.velocity == 0 or message.type == "note_off":
                        notes_sequence.append(
                            Note(message.note,
                                 self._bucket_duration(time - note_start_time[message.note])))
                    # If the note is on
                    else:
                        note_start_time[message.note] = time
        # Add every pair of adjacent notes to the markov chain
        for i in range(len(notes_sequence) - ORDER):
            self.markov_chain.add(tuple(notes_sequence[i: i+ORDER]), notes_sequence[i+ORDER])


    def _bucket_duration(self, ticks):
        """
        This method takes a tick count and converts it to a time in
        milliseconds, bucketing it to the nearest 30 milliseconds.
        """
        try:
            ms = ((ticks / self.ticks_per_beat) * self.tempo) / 1000
            return int(ms - (ms % 30) + 30)
        except TypeError:
            raise TypeError(
                "Could not read a tempo and ticks_per_beat from midi")

    def get_chain(self):
        return self.markov_chain

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The midi file input")
    args = parser.parse_args()
    print(Parser(args.input_file, verbose=False).get_chain())
    print('No issues parsing {}'.format(args.input_file))