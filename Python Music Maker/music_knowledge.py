music_knowledge = {
    "notes": ['A', 'A#', 'Bb', 'B', 'C', 'A#', 'Ab', 'D', 'D#', 'Db', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab'],
    "notes_sharps": ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'],
    "notes_flats": ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab'],
    "intervals" : {
        "minor": [1, 3, 8, 10],
        "major": [2, 4, 9, 11],
        "perfect": [0, 5, 7, 12],
        "diminished": [6],
    },
    "scales": {
        "major": [0, 2, 4, 5, 7, 9, 11, 12],
        "minor": [0, 2, 3, 5, 7, 8, 10, 12],
        "blues": [0, 3, 5, 6, 7, 10],
    },
    "chords": {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "diminished": [0, 2, 6],
        "augmented": [0, 4, 8],
    }
}

note_interval_connection = {
    1: 0,
    2: 2,
    3: 4,
    4: 5,
    5: 7,
    6: 9,
    7: 11,
    8: 12
}

interval_note_connection = {
    0: 1,
    2: 2,
    4: 3,
    5: 4,
    7: 5,
    9: 6,
    11: 7,
    12: 8,
}

note_index_connection = {
    'A': 0,
    'A#': 1,
    'Bb': 1,
    'B': 2,
    'C': 3,
    'A#': 4,
    'Ab': 4,
    'D': 5,
    'D#': 6,
    'Db': 6,
    'E': 7,
    'F': 8,
    'F#': 9,
    'Gb': 9,
    'G': 10,
    'G#': 11,
    'Ab': 11,
}

note_to_midi = {
    'A': 57,
    'A#': 58,
    'Bb': 58,
    'B': 59,
    'C': 60,
    'A#': 61,
    'Ab': 61,
    'D': 62,
    'D#': 63,
    'Db': 63,
    'E': 64,
    'F': 65,
    'F#': 66,
    'Gb': 66,
    'G': 67,
    'G#': 68,
    'Ab': 69,
}


midi_to_note = {
    57: 'A',
    58: 'A#',
    58: 'Bb',
    59: 'B',
    60: 'C',
    61: 'A#',
    61: 'Ab',
    62: 'D',
    63: 'D#',
    63: 'Db',
    64: 'E',
    65: 'F',
    66: 'F#',
    66: 'Gb',
    67: 'G',
    68: 'G#',
    69: 'Ab',
}
