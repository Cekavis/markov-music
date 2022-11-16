from markov_chain import MarkovChain
from generator import Generator

import random
import mido

class Mixer(Generator):

    def __init__(self):
        pass
    
    @staticmethod
    def load(markov_chain1, markov_chain2):
        assert isinstance(markov_chain1, MarkovChain)
        assert isinstance(markov_chain2, MarkovChain)
        markov_chain1.merge(markov_chain2)
        markov_chain1.print_as_matrix()
        return Generator(markov_chain1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        # Example usage:
        # python generator.py <in.mid1> <in.mid2> <out.mid>
        from midi_parser import Parser
        chain1 = Parser(sys.argv[1]).get_chain()
        print('Generated markov chain1')
        chain2 = Parser(sys.argv[2]).get_chain()
        print('Generated markov chain2')
        Mixer.load(chain1, chain2).generate(sys.argv[3])
        print('Generated markov chain')
        
    else:
        print('Invalid number of arguments:')
        print('Example usage: python generator.py <in1.mid> <in2.mid> <out.mid>')
