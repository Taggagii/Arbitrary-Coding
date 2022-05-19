from music_knowledge import *
from midiutil.MidiFile import MIDIFile
import os
import pygame



#general track making stuff
midi_file = MIDIFile(1)
track = 0
start_time = 0
tempo = 240
midi_file.addTrackName(track, start_time, "Fucker")
midi_file.addTempo(track, start_time, tempo)
channel = 0
volume = 100

def chord_maker(starting_note, chord_type):
    starting_note = starting_note.capitalize()
    if starting_note not in music_knowledge["notes"]:
        return "Your starting note must exist"
    if chord_type not in music_knowledge["chords"]:
        return "Your chord type must exist"
    chord_values = music_knowledge["chords"][chord_type]
    #build the chord
    index = note_index_connection[starting_note]
    chord1 = [music_knowledge["notes_flats"][(index + interval) % 12] for interval in chord_values]
    chord2 = [music_knowledge["notes_sharps"][(index + interval) % 12] for interval in chord_values]
    notes = [index + interval for interval in chord_values]
    return notes


def build_chord_from_note(note, chord, numeric_value = False):
    if not numeric_value:
        note = note.capitalize()
        chord = chord_maker(note, chord)
        note = note_to_midi[note]
    else:
        chord = chord_maker(midi_to_note[note], chord)
    return [note + i for i in chord]


lastTime = 0
def add_note(pitch, time = None, duration = 1):
    global lastTime
    if time is not None:
        if time > lastTime:
            lastTime = time
    else:
        lastTime += 1
        time =  lastTime
    midi_file.addNote(track,  channel, pitch, time, duration, volume)

def add_chord(pitches, time = None, duration = 1):
    global lastTime
    if time is not None:
        if time > lastTime:
            lastTime = time
    else:
        lastTime += 1
        time =  lastTime
    for pitch in pitches:
        add_note(pitch, time, duration)


origin = 65

# for i in values:
#     add_chord([origin + x for x in i], counter, 1)
#     counter += 1
# for i in music_knowledge['scales']['blues']:
#     add_note(i + origin, counter, 1)
#     counter += 1

counter = 6
for i in [('Bb', 'major'), ('e', 'major')]:
    add_chord(build_chord_from_note(i[0], i[1]))
    
# add_note(music_knowledge['scales']['blues'][0] + origin + 12, counter, 5)

'''
perfect unison = 0
minor 2nd = 1
major 2nd = 2
major 3rd = 4
minor 3rd = 3
perfect fourth = 5
augmented fourth = 6
perfect fifth = 7
minor sixth = 8
major sixth = 9
minor 7th = 10
major 7th = 11
perfect unison / octave = 12
'''
while True:
    try:
        with open("output.mid", "wb") as outputFile:
            midi_file.writeFile(outputFile)
        break
    except:
        pass
        os.system("TASKKILL /F /IM wmplayer.exe")
##
##
##os.system("output.mid")

pygame.mixer.init(441, -16, 2, 1024)
pygame.mixer.music.load("output.mid")
pygame.mixer.music.play()
