from music_knowledge import *
from midiutil.MidiFile import MIDIFile
import os
import pygame
import random



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
        lastTime += duration
        time =  lastTime
    midi_file.addNote(track, channel, pitch, time, duration, volume)

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

def add_random_scale(origin = 63):
    scale = music_knowledge["scales"][random.choice(list(music_knowledge["scales"].keys()))]
    for i in scale:
        add_note(i + origin, duration = 1, increase_amount = random.randint(1, 2))

def add_random_sequence_from_scale(scale = None, length = None, origin = 63, random_origin = True, origin_change_frequency = 8):
    if (scale is None):
        scale = music_knowledge["scales"][random.choice(list(music_knowledge["scales"].keys()))]
    else:
        scale = music_knowledge["scales"][scale]
    if (length is None):
        length = random.randint(0, 50)
    origin_change_counter = 0
    value = random.randint(1, 80) / 10
    for i in range(length):
        if random_origin and origin_change_counter == origin_change_frequency:
            origin = random.randint(20, 100)
            origin_change_counter = 0
            value = random.randint(1, 10) / 10
        add_note(random.choice(scale) + origin, duration = value)
        origin_change_counter += 1

def add_random_chord():
    chord_type = random.choice(list(music_knowledge["chords"].keys()))
    starting_note = random.choice(music_knowledge["notes"])
    add_chord(build_chord_from_note(starting_note, chord_type))

def add_random_note():
    starting_note = music_knowledge["notes"]
    print(music_knowledge)

##add_random_note()
##for i in range(100):
##    add_random_chord()

for i in range(1000):
    add_random_sequence_from_scale()
##    for ii in range(random.randint(0, 1)):
##        add_random_chord()


origin = 50
##for i in values:
##    add_chord([origin + x for x in i], counter, 1)
##    counter += 1




##counter = 6
##for i in [('Bb', 'major'), ('e', 'major'), ('f', 'minor'), ('g', 'diminished'), ('f#', 'minor'), ('c', 'major'), ('d', 'minor]:
##    add_chord(build_chord_from_note(i[0], i[1]))
counter = 6
    
##add_note(music_knowledge['scales']['blues'][0] + origin + 12, counter, 5)

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
