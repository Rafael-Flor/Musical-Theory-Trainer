class Note: #Nota musical

    def __init__(self, pitch, name):

        if pitch in range(0,128):
            self.pitch=pitch #Tom da nota em semitons
            self.name=name

        else:
            raise ValueError(f"Invalid pitch value {pitch}")


class ScaleType: #Formato genérico para um tipo de escala
    def __init__(self, name, scale_degrees, note_steps):
        self.name=name
        self.scale_degrees = scale_degrees #graus da escala
        self.note_steps=note_steps #intervalos entre graus da escala em semitons


class MusicTheoryModel:
    NATURAL_NOTE_NAMES=["C","D","E","F","G","A","B"]
    TONICS = [
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
        Note(11, "B")] #Tónicas possiveis
    def __init__(self):
        self.scale_types=[ #Definição dos tipos de escala do modelo
            ScaleType("Major", [1, 2, 3, 4, 5, 6, 7], [2, 2, 1, 2, 2, 2, 1]),
            ScaleType("Minor", [1, 2, 3, 4, 5, 6, 7], [2, 1, 2, 2, 1, 2, 2]),
            ScaleType("Major Pentatonic", [1, 2, 3, 5, 6], [2, 2, 3, 2]),
            ScaleType("Minor Pentatonic", [1, 3, 4, 5, 7], [3, 2, 2, 3]),
            ScaleType("Mixolydian", [1, 2, 3, 4, 5, 6, 7], [2, 2, 1, 2, 2, 1, 2]),
            ScaleType("Dorian", [1, 2, 3, 4, 5, 6, 7],[2, 1, 2, 2, 2, 1, 2])
        ]


