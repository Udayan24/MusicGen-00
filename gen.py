'''
Required Libraries: 
- PyO: Generating Audio
- MIDIUtil: Generating MIDI files
- CLICK (CLI Creation Kit): Creating CLI menus
'''
# ---- MUSIC GENERATOR 0.0 ---- 
from pyo import *
from midiutil import MidiFile
from datetime import datetime
from typing import List, Dict
import click

from random import choices

# ----- GLOBAL VARIABLES ---------------------------------------------
bars = 1
steps = 1
pauses = True
population_size = 5
nMutation = 2
probMutation = 0.5

BITS_PER_NOTE = 4
# --------------------------------------------------------------------

Genome = List[int]

def createGenome(length) -> Genome:
    return choices([0, 1], k=length)

# ----- FUNCTIONS ----------------------------------------------------
def melodyGen(genome, bars, notes, steps, pauses, key, scale, root) -> Dict[str, list]:
    notes = [genome[i * BITS_PER_NOTE:i * BITS_PER_NOTE + BITS_PER_NOTE] for i in range(bars*notes)]
    print(notes)

def save_to_midi(filename, genome, notes, key, scale, root, bpm):
    melody = melodyGen(genome, bars, notes, steps, pauses, key, scale, root)
    
    
    
    return 0

# ----- CLI Interface ------------------------------------------------
KEYS=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SCALES=["major", "minor"]

@click.command()
@click.option("--notes", default=4, prompt='Notes per bar:', type=int)
@click.option("--key", default="C", prompt='Key:', type=click.Choice(KEYS, case_sensitive=False))
@click.option("--scale", default="major", prompt='Scale:', type=click.Choice(SCALES, case_sensitive=False))
@click.option("--root", default=3, prompt='Scale Root:', type=int)
@click.option("--bpm", default=128, type=int)
# --------------------------------------------------------------------

def main(notes:int, key:str, scale:str, root:int, bpm:int):
    folderStr = datetime.now()
    folderName = folderStr.strftime("%d%m_%H%M")

    #s = Server().boot()
    for i in range(4):
        genome = createGenome(bars*notes*BITS_PER_NOTE)
        print(genome)
        print(genome.__len__())
        print()
    # melodyGen(genome, bars, notes, steps, pauses, key, scale, root)

if __name__ == '__main__':
    main()