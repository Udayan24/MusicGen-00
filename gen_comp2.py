'''
MUSIC GENERATOR 0.0 - COMPONENT 2
BE-PROJECT 2023: 41102, 41113, 41117
'''
# Import required libraries
from pyo import *
from typing import List, Dict
from random import choices

# -----------------------------------------------------------------------------
bars = 8
N_notes = 4             # {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} where each N ~ 1011 (4 bits per note)
bits_per_note = 4       # More bits_per_note => More variation in notes. Currently will select random 16 notes 

# -----------------------------------------------------------------------------
def eventGen(genome, bits_per_note=bits_per_note, N_notes=N_notes) -> Events:
    
    # Create a list of notes taking 4 values out of genome at a time
    notes = [genome[i:i+bits_per_note] for i in range(N_notes)]

    for n in notes:
        print(n)

    freqList = [50+sum([bit*pow(2,index) for index, bit in enumerate(note)]) for note in notes]
    print("Frequencies generated:", freqList)
       
    return Events(
        midinote = EventSeq(freqList, occurrences=1),
        beat=1/4.
    )

# -----------------------------------------------------------------------------
def eventGen2(genome, bars, N_notes, steps, key, scale, root):
    melody = melodyGen(genome, bars, N_notes, steps, key, scale, root)
    print("Genome:", genome)
    print("Bars:", bars)
    print("Notes:", N_notes)
    print("Steps:", steps)
    print("Key:", key)
    print("Scale:", scale)
    print("Root:", root)
    print("Notesss: ", melody['notes'])

    return [
        Events(
            midinote=EventSeq(step, occurrences=1),
            midivel=EventSeq(melody["velocity"], occurrences=1),
            beat=EventSeq(melody["beat"], occurrences=1),
            attack=0.001,
            decay=0.05,
            sustain=0.5,
            release=0.005,
        ) for step in melody["notes"]
    ]

# --------------------------------------------------------------------------------
def intGen(bits: List[int]) -> int:
    return int(sum([bit*pow(2,index) for index, bit in enumerate(bits)]))

def melodyGen(genome, bars, N_notes, n_steps, key, scale, root) -> Dict[str, list]:
    notes = [genome[i:i+bits_per_note] for i in range(N_notes*bars)]
    print("Notes:", notes)

    # 1 bar => 4 notes.
    note_length = 4 / float(N_notes)

    #       Construct a list of pitches according to arguments
    scl = EventScale(root=key, scale=scale, first=root)

    #       Melody is represented by a dictionary. 
    melody = {
        "notes": [],
        "velocity": [],
        "beat": []
    }

    for note in notes:
        integer = intGen(note)

        if integer >= pow(2, bits_per_note-1):
            melody["notes"] += [0]
            melody["velocity"] += [0]
            melody["beat"] += [note_length]
        else:
            if len(melody["notes"]) > 0 and melody["notes"][-1] == integer:
                melody["beat"][-1] += note_length
            else:
                melody["notes"] += [integer]
                melody["velocity"] += [127]
                melody["beat"] += [note_length]
    
    print("-----------------------")
    print("Notes:", melody['notes'])

    steps = []
    for step in range(n_steps):
        steps.append([scl[(note+step*2) % len(scl)] for note in melody["notes"]])

    melody["notes"] = steps
    print(melody['notes'])

    return melody

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
Genome = List[int]

def createGenome(length) -> Genome:
    return choices([0, 1], k=length)    # returns array of length k with random 0/1 values

# --------------------------------------------------------------------------------
# Create a new genome (melody) of required length (currently 4(bits per note) * 4(notes per bar) * 8(bars) = 128 bits)

genome = createGenome(bars*N_notes*bits_per_note)
print("Genome:", genome)

# -------------------------------------------------------------------------------
# Create PyO server and an event with our genome
s=Server().boot()

#e=eventGen(genome)
#e.play()

print("-----------------------")
key="D"
scale="minor"
root=4
steps=2


# Play a melody in D minor scale
'''
scl = EventScale(root="D", scale="minorM", type=2)
f = Events(degree=EventDrunk(scl, maxStep=2, occurrences=N_notes), beat=1/4.).play()
'''


eventss=eventGen2(genome, bars, N_notes, steps, key, scale, root)
for e in eventss:
    e.play()

s.gui(locals())