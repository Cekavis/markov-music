#!/usr/bin/python
# This class handles the storage and manipulation of a markov chain of notes.
# v2: Record the duration of both 'from_note' and 'to_note' in the transition

from collections import Counter, defaultdict, namedtuple

import random

Note = namedtuple('Note', ['note', 'duration'])

ORDER = 3

class MarkovChain:

    def __init__(self):
        self.chain = defaultdict(Counter)
        self.sums = defaultdict(int)

    def __str__(self):
        return str(self.get_chain())

    def add(self, from_notes, to_note):
        self.chain[from_notes][to_note] += 1
        self.sums[from_notes] += 1

    def get_next(self, seed_notes):
        if seed_notes is None or seed_notes not in self.chain:
            random_chain = self.chain[random.choice(list(self.chain.keys()))]
            return random.choice(list(random_chain.keys()))
        next_note_counter = random.randint(0, self.sums[seed_notes])
        for note, frequency in self.chain[seed_notes].items():
            next_note_counter -= frequency
            if next_note_counter <= 0:
                return note

    def merge(self, other):
        assert isinstance(other, MarkovChain)
        self.sums = defaultdict(int)
        for from_notes, to_notes in other.chain.items():
            self.chain[from_notes].update(to_notes)
        for from_notes, to_notes in self.chain.items():
            self.sums[from_notes] = sum(self.chain[from_notes].values())

    def get_chain(self):
        return {k: dict(v) for k, v in self.chain.items()}

    def print_as_matrix(self, limit=10):
        columns = []
        for from_notes, to_notes in self.chain.items():
            for note in to_notes:
                if note not in columns:
                    columns.append(note)
        _col = lambda string: '{:<8}'.format(string)
        _note = lambda note: '{}:{}'.format(note.note, note.duration)
        out = _col('')
        out += ''.join([_col(_note(note)) for note in columns[:limit]]) + '\n'
        for from_notes, to_notes in self.chain.items():
            out += _col('+'.join([_note(x) for x in from_notes]))
            for note in columns[:limit]:
                out += _col(to_notes[note])
            out += '\n'
        print(out)
