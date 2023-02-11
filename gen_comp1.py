'''
MUSIC GENERATOR 0.0 - COMPONENT 1
BE-PROJECT 2023: 41102, 41113, 41117
'''
# Import required libraries
from pyo import *
from typing import List, Dict
from random import choices
# -----------------------------------------------------------------------------
# Set number of notes and representation of a note as 16 bits.
# 0000, 0001, 0010, 0011, 0100, 0101, 0110, 0111
# 1000, 1001, 1010, 1011, 1100, 1101, 1110, 1111

N_notes = 4*8           # {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} where each N ~ 1011 (4 bits per note)
bits_per_note = 4       # More bits_per_note => More variation in notes. Currently will select random 16 notes 
# -----------------------------------------------------------------------------

'''
PyO works on an Event framework. Allows users generate a sequence of
events. Events object computes parameters, builds events and plays the sequence.
'''

def eventGen(genome, bits_per_note=bits_per_note, N_notes=N_notes) -> Events:
    
    # Create a list of notes taking 4 values out of genome at a time
    notes = [genome[i:i+bits_per_note] for i in range(N_notes)]

    for n in notes:
        print(n)

        #       EventSeq plays through an entire list of values. takes (values, occurrences)
        #       values: List of values to loop over, occurences: Number of times sequence is looped
        
        #       [50+sum([bit*pow(2,index) for index, bit in enumerate(note)]) for note in notes]
        #        50+sum([bit*pow(2,index) for index, bit in enumerate(note)]) for each [1, 0, 1, 1]

        #        sum([bit*pow(2,index) for index, bit in enumerate(note)]) 
        #        [1, 0, 1, 1] => 1*(2^0) + 0*(2^1) + 1*(2^2) + 1*(2^3) = 1 + 4 + 8 = 13
    
    freqList = [50+sum([bit*pow(2,index) for index, bit in enumerate(note)]) for note in notes]
    print("Frequencies generated:", freqList)
       
    return Events(
        midinote = EventSeq(freqList, occurrences=1),
        beat=1/4.
    )

# --------------------------------------------------------------------------------
Genome = List[int]

def createGenome(length) -> Genome:
    return choices([0, 1], k=length)    # returns array of length k with random 0/1 values

# --------------------------------------------------------------------------------
# Create a new genome (melody) of required length (currently 4(bits per note) * 4(notes per bar) * 8(bars) = 128 bits)

genome = createGenome(N_notes*bits_per_note)
print("Current Genome:", genome)

# -------------------------------------------------------------------------------
# Create PyO server and an event with our genome
s=Server().boot()

e=eventGen(genome)
e.play()

s.gui(locals())