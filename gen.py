'''
Required Libraries: 
- PyO: Generating Audio
- MIDIUtil: Generating MIDI files
- CLICK (CLI Creation Kit): Creating CLI menus
'''
# ---- MUSIC GENERATOR 0.0 ---- #
from pyo import *
from midiutil import MidiFile
from datetime import datetime
import click

KEYS=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SCALES=["major", "minor"]

@click.command()
@click.option("--notes", default=4, prompt='Notes per bar:', type=int)
@click.option("--key", default="C", prompt='Key:', type=click.Choice(KEYS, case_sensitive=False))
@click.option("--scale", default="major", prompt='Scale:', type=click.Choice(SCALES, case_sensitive=False))
@click.option("--root", default=4, prompt='Scale Root:', type=int)
@click.option("--bpm", default=128, type=int)


def main(notes:int, key:str, scale:str, root:int, bpm:int):
    print("hello")

if __name__ == '__main__':
    main()