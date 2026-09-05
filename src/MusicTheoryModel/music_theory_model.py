class Note: #Nota musical

    def __init__(self, pitch):
        if pitch in range(0,128):
            self.pitch=pitch #Tom da nota em semitons
        else:
            raise ValueError(f"Invalid pitch value {pitch}")


    def __add__(self, offset): #Adição de uma nota com um inteiro resulta na elevação do seu tom por esse valor
        if isinstance(offset, int):
            return Note(self.pitch+offset)
        else:
            return NotImplemented


class ScaleType: #Formato genérico para um tipo de escala
    def __init__(self, name, scale_degrees, note_offsets):
        self.name=name
        self.scale_degrees = scale_degrees #graus da escala
        self.note_offsets=note_offsets #distancia de cada nota da escala à tónica


class MusicTheoryModel:
    TONICS = [Note(0), Note(1), Note(2), Note(3), Note(4), Note(5), Note(6), Note(7), Note(8), Note(9), Note(10), Note(11)] #Tónicas possiveis
    def __init__(self):
        self.scale_types=[ #Definição dos tipos de escala do modelo
            ScaleType("Major", [0, 1, 2, 3, 4, 5, 6], [0, 2, 4, 5, 7, 9, 11, 12]),
            ScaleType("Minor", [0, 1, 2, 3, 4, 5, 6], [0, 2, 3, 5, 7, 8, 10, 12]),
            ScaleType("Major Pentatonic", [0, 1, 2, 4, 5], [0, 2, 4, 7, 9]),
            ScaleType("Minor Pentatonic", [0, 2, 3, 4, 6], [0, 3, 5, 7, 10]),
            ScaleType("Mixolydian", [0, 1, 2, 3, 4, 5, 6], [0, 2, 4, 5, 7, 9, 10, 12]),
            ScaleType("Dorian", [0, 1, 2, 3, 4, 5, 6],[0, 2, 3, 5, 7, 9, 10, 12])
        ]


