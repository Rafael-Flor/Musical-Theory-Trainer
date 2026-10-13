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

class ProgDegreeSet: #Conjunto de graus que podem compor uma progressão harmónica
    def __init__(self, name, chord_types, chord_degrees, mode):
        self.name=name
        self.chord_types=chord_types
        self.chord_degrees=chord_degrees
        self.mode=mode

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
            ChordType("Halfdiminished7", [1, 3, 5, 7], [3, 3, 4]),
            ChordType("Sus2", [1, 2, 5], [2, 5]),
            ChordType("Sus4", [1, 4, 5], [5, 2]),
        ]
        self.prog_degrees=[     #Definição dos conjuntos de graus para compor progressões harmónicas
            ProgDegreeSet("MajorDiatonics",{"I": "Major", "ii": "Minor", "iii": "Minor", "IV": "Major", "V": "Major", "vi": "Minor","viiº": "Diminished"},[1,2,3,4,5,6,7],"Major"),
            ProgDegreeSet("Major7thDiatonics", {"Imaj7": "Major7", "ii7": "Minor7", "iii7": "Minor7", "IVmaj7": "Major7", "V7": "7","vi7": "Minor7", "viiø7": "Halfdiminished7"}, [1,2,3,4,5,6,7],"Major"),
            ProgDegreeSet("MinorDiatonics",{"i": "Minor", "iiº": "Diminished", "III": "Major", "iv": "Minor", "v": "Minor","VI": "Major", "VII": "Major"}, [1, 2, 3, 4, 5, 6, 7], "Minor"),
            ProgDegreeSet("Minor7thDiatonics",  {"i7": "Minor7", "iiø7": "Halfdiminished7", "IIImaj7": "Major7", "iv7": "Minor7", "v7": "Minor7","VImaj7": "Major7", "VII7": "7"}, [1, 2, 3, 4, 5, 6, 7], "Minor"),
            ProgDegreeSet("MajorSus2",{"Isus2": "Sus2", "iisus2": "Sus2", "IVsus2": "Sus2", "Vsus2": "Sus2"}, [1,2,4,5], "Major"),
            ProgDegreeSet("MajorSus4", {"Isus4": "Sus4", "iisus4": "Sus4", "IVsus4": "Sus4", "Vsus4": "Sus4"},[1, 2, 4, 5], "Major"),
            ProgDegreeSet("MinorSus2", {"isus2": "Sus2", "iisus2": "Sus2", "ivsus2": "Sus2", "vsus2": "Sus2"}, [1, 2, 4, 5], "Minor"),
            ProgDegreeSet("MinorSus4", {"isus4": "Sus4", "iisus4": "Sus4", "ivsus4": "Sus4", "vsus4": "Sus4"},[1, 2, 4, 5], "Minor")
        ]



