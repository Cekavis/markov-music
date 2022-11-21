#!/usr/bin/python
# This class handles the generation of a new song given a markov chain
# containing the note transitions and their frequencies.

from markov_chain import MarkovChain, ORDER

import random
import mido

class Generator:

    def __init__(self, markov_chain):
        self.markov_chain = markov_chain

    @staticmethod
    def load(markov_chain):
        assert isinstance(markov_chain, MarkovChain)
        return Generator(markov_chain)

    def _note_to_messages(self, note):
        return [
            mido.Message('note_on', note=note.note, velocity=127,
                         time=0),
            mido.Message('note_off', note=note.note, velocity=0,
                         time=note.duration)
        ]

    def generate(self, filename):
        with mido.midifiles.MidiFile() as midi:
            track = mido.MidiTrack()
            # Select a random starting notes sequence
            valid_starting_notes = list(self.markov_chain.chain.keys())
            melody = list(random.choice(valid_starting_notes))
            # Generate a sequence of 100 notes
            for i in range(100):
                new_note = self.markov_chain.get_next(tuple(melody[-ORDER:]))
                melody.append(new_note)
                track.extend(self._note_to_messages(new_note))
            midi.tracks.append(track)
            midi.save(filename)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        # Example usage:
        # python generator.py <in.mid> <out.mid>
        from midi_parser import Parser
        chain = Parser(sys.argv[1]).get_chain()
        Generator.load(chain).generate(sys.argv[2])
        chain.print_as_matrix()
        print('Generated markov chain')
    else:
        print('Invalid number of arguments:')
        print('Example usage: python generator.py <in.mid> <out.mid>')
