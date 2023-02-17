'''
MUSIC GENERATOR 0.0 - COMPONENT 3
BE-PROJECT 2023: 41102, 41113, 41117
'''
# Import required libraries
from pyo import *
from typing import List, Dict
from random import choices
from midiutil import MIDIFile

# -----------------------------------------------------------------------------
# PARAMETERS:
bars = 8
N_notes = 4             # {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} {N|N|N|N} where each N ~ 1011 (4 bits per note)
bits_per_note = 4       # More bits_per_note => More variation in notes. Currently will select random 16 notes 
key="G"
scale="minorM"
root=3
steps=1

bpm=128

# -----------------------------------------------------------------------------
def eventGen(genome, bars, N_notes, steps, key, scale, root):
    melody = melodyGen(genome, bars, N_notes, steps, key, scale, root)
    print("\nGenome:", genome)
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
            sustain=3,
            release=0.005,
            bpm=128
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
        print("steps:", [scl[(note+step*2) % len(scl)] for note in melody["notes"]])

    melody["notes"] = steps
    print("Final melody:", melody['notes'])
    print(len(scl))

    return melody

# --------------------------------------------------------------------------------
def save_genome_to_midi(filename, genome, num_bars, num_notes, num_steps, key, scale, root, bpm):
    
    # Generate a melody dictionary
    melody = melodyGen(genome, num_bars, num_notes, num_steps, key, scale, root)

    # Check if all lists are of same size
    if len(melody["notes"][0]) != len(melody["beat"]) or len(melody["notes"][0]) != len(melody["velocity"]):
        raise ValueError

    # Create a single track
    mf = MIDIFile(1)

    track = 0
    channel = 0
    time = 0.0

    # Create a track and add file tempo
    mf.addTrackName(track, time, "Generated Track")
    mf.addTempo(track, time, bpm)

    # Go through velocity list and add each note with non-zero volume
    for i, vel in enumerate(melody["velocity"]):
        if vel > 0:
            for step in melody["notes"]:
                mf.addNote(track, channel, step[i], time, melody["beat"][i], vel)

        time += melody["beat"][i]

    # Create a file called filename
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        mf.writeFile(f)

# --------------------------------------------------------------------------------
def metronome(bpm: int):
    met = Metro(time=1 / (bpm / 60.0)).play()
    t = CosTable([(0, 0), (50, 1), (200, .3), (500, 0)])
    amp = TrigEnv(met, table=t, dur=.25, mul=1)
    freq = Iter(met, choice=[660, 440, 440, 440])
    return Sine(freq=freq, mul=amp).mix(2).out()
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

m=metronome(bpm)

eventss=eventGen(genome, bars, N_notes, steps, key, scale, root)
for e in eventss:
    e.play()

save_genome_to_midi("C:\\Users\\udaya\\Documents\\000_BE_PROJECT\\PROJECT\\MIDI\\1.mid", genome, bars, N_notes, steps, key, scale, root, bpm)

s.gui(locals())