class Note: #Nota musical

    def __init__(self, pitch, name):

        if pitch in range(0,128):
            self.pitch=pitch #Tom da nota em semitons
            self.name=name

        else:
            raise ValueError(f"Invalid pitch value {pitch}")


class Scale: #Escala musical
    def __init__(self, tonic, scale_type, notes):
        self.tonic=tonic
        self.scale_type=scale_type
        self.notes=notes

class Chord: #Acorde
    def __init__(self, tonic, chord_type, notes):
        self.tonic=tonic
        self.chord_type=chord_type
        self.notes=notes

class ChordProg: #Progressão Harmónica
    def __init__(self, scale, prog_type, prog_chords):
        self.scale=scale
        self.prog_type=prog_type
        self.prog_chords=prog_chords

class ScaleType: #Formato genérico para um tipo de escala
    def __init__(self, name, scale_degrees, note_steps):
        self.name=name
        self.scale_degrees = scale_degrees #graus da escala
        self.note_steps=note_steps #intervalos entre graus da escala, em semitons

class ChordType: #Formato genérico para um tipo de acorde
    def __init__(self, name, chord_degrees, note_steps):
        self.name=name
        self.chord_degrees=chord_degrees
        self.note_steps=note_steps

class ChordProgType: #Formato genérico para um tipo de progressão harmónica
    def __init__(self, name, chord_types, prog_degrees):
        self.name=name
        self.chord_types=chord_types
        self.prog_degrees=prog_degrees

class MusicTheoryModel:
    NATURAL_NOTE_NAMES=["C","D","E","F","G","A","B"]
    TONICS = (
        Note(0, "C"),
        Note(1, "C#"),
        Note(1, "Db"),
        Note(2,"D"),
        Note(3, "D#"),
        Note(3, "Eb"),
        Note(4, "E"),
        Note(5, "F"),
        Note(6, "F#"),
        Note(6, "Gb"),
        Note(7, "G"),
        Note(8, "G#"),
        Note(8, "Ab"),
        Note(9, "A"),
        Note(10, "A#"),
        Note(10, "Bb"),
        Note(11, "B"))
    def __init__(self):
        self.scale_types=[          #Definição dos tipos de escala do modelo
            ScaleType("Major", [1, 2, 3, 4, 5, 6, 7], [2, 2, 1, 2, 2, 2, 1]),
            ScaleType("Minor", [1, 2, 3, 4, 5, 6, 7], [2, 1, 2, 2, 1, 2, 2]),
            ScaleType("Major Pentatonic", [1, 2, 3, 5, 6], [2, 2, 3, 2]),
            ScaleType("Minor Pentatonic", [1, 3, 4, 5, 7], [3, 2, 2, 3]),
            ScaleType("Mixolydian", [1, 2, 3, 4, 5, 6, 7], [2, 2, 1, 2, 2, 1, 2]),
            ScaleType("Dorian", [1, 2, 3, 4, 5, 6, 7],[2, 1, 2, 2, 2, 1, 2])
        ]
        self.chord_types=[          #Definição dos tipos de acordes do modelo
            ChordType("Major", [1, 3, 5], [4,3]),
            ChordType("Minor", [1, 3, 5], [3, 4]),
            ChordType("Major7", [1, 3, 5, 7], [4, 3, 4]),
            ChordType("Minor7", [1, 3, 5, 7], [3, 4, 3]),
            ChordType("7", [1, 3, 5, 7], [4,3, 3]),
            ChordType("Diminished", [1, 3, 5], [3, 3]),
            ChordType("Diminished7", [1, 3, 5, 7], [3, 3, 3]),
        ]
        self.chord_prog_types=[     #Definição dos tipos de progressões do modelo
            ChordProgType("I-V", ("Major","Major"), [1,5]),
            ChordProgType("I-IV", ("Major", "Major"), [1,4]),
            ChordProgType("I-vi", ("Major", "Minor"), [1,6]),
            ChordProgType("ii-V", ("Minor", "Major"), [2,5]),
            ChordProgType("vi-IV", ("Minor", "Major"), [6,4]),
            ChordProgType("ii-V7-I", ("Minor", "7", "Major"), [2,5,1]),
        ]


