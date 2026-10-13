
from src.MusicTheoryModel.music_theory_model import Scale, Note, Chord, ChordProg, ChordProgType

import random

class Exercise:
    def __init__(self, title, correct_answer, wrong_answers, explanation):
        self.title = title
        self.wrong_options = wrong_answers
        self.correct_answer = correct_answer
        self.explanation = explanation

class IntervalScaleExercise(Exercise):

    def __init__(self, scale, interval_note, title, correct_answer, wrong_answers, explanation):
        super().__init__(title, correct_answer, wrong_answers, explanation)
        self.scale=scale
        self.interval_note=interval_note

    def __str__(self):
        note_names="|".join(note.name for note in self.scale.notes)
        return (f"--------------\n"
                f"Titulo: {self.title}\n"
                f"Escala: {self.scale.tonic.name} {self.scale.scale_type.name}\n"
                f"Notas da escala {note_names}\n"
                f"Opção correta: {self.correct_answer}\n"
                f"Opções erradas: {self.wrong_options}\n"
                f"Explicação: {self.explanation}")

class ProgressionExercise(Exercise):
    def __init__(self, progression, title, correct_answer, wrong_answers, explanation):
        super().__init__(title, correct_answer, wrong_answers, explanation)
        self.progression=progression

    def __str__(self):
        chord_names=[]
        for chord in self.progression.prog_chords:
            chord_names.append(f"{chord.tonic.name} {chord.chord_type.name}")
        prog_info=f"{self.progression.prog_type.name} na tonalidade de {self.progression.scale.tonic.name} {self.progression.scale.scale_type.name} "
        return (f"--------------\n"
                f"Titulo: {self.title}\n"
                f"Progressão: {prog_info}\n"
                f"Acordes: {"-".join(chord_names)}\n"
                f"Opção correta: {self.correct_answer}\n"
                f"Opções erradas: {self.wrong_options}\n"
                f"Explicação: {self.explanation}")

class ChordExercise(Exercise):
    def __init__(self, chord, title, correct_answer, wrong_answers, explanation):
        super().__init__(title, correct_answer, wrong_answers, explanation)
        self.chord=chord

    def __str__(self):
        note_names=[]
        for note in self.chord.notes:
            note_names.append(note.name)
        chord_info=f"{self.chord.tonic.name} {self.chord.chord_type.name}\n"
        return (f"--------------\n"
                f"Titulo: {self.title}\n"
                f"Acorde: {chord_info}\n"
                f"Notas: {"-".join(note_names)}\n"
                f"Opção correta: {self.correct_answer}\n"
                f"Opções erradas: {self.wrong_options}\n"
                f"Explicação: {self.explanation}")

class ExerciseGenerator: #Gerador de exercicios
    scale_difficulty_settings = {"easy": ("Major",), "medium": ("Major", "Minor"), "hard" :("Major", "Minor", "Major Pentatonic", "Minor Pentatonic", "Mixolydian", "Dorian")} #Definições de dificuldade relativas ao tipo de escala
    prog_difficulty_settings = {"easy":("MajorDiatonics","MinorDiatonics"),
                                "medium":("MajorDiatonics","MinorDiatonics","Major7thDiatonics","Minor7thDiatonics"),
                                "hard":("MajorDiatonics","MinorDiatonics","Major7thDiatonics","Minor7thDiatonics","MajorSus2","MinorSus2","MajorSus4","MinorSus4")}
    prog_len_difficulty_settings = {"easy":(2,),"medium":(2,3,4),"hard": (4,5,6)}
    chord_difficulty_settings ={"easy":("Major","Minor"), "medium":("Major","Minor","Major7","Minor7","7"),"hard":("Major","Minor","Major7","Minor7","7","Diminished","Diminished7","Halfdiminished7","Sus2","Sus4")}

    def __init__(self, theory_model):
        self.theory_model=theory_model #Modelo de teoria que o gerador utiliza

    def generate_scale_interval_exercise(self, difficulty, generate_options=True): #Gera um exercicio de reconhecimento de intervalos em escalas
        scale=self.generate_scale(difficulty) #Gerar uma escala
        interval_note=random.choice(scale.notes[1:]) #Escolher uma nota da escala para obter o intervalo do exercicio
        interval_note_index=scale.notes.index(interval_note) #Grau da nota do intervalo
        interval_note_degree=scale.scale_type.scale_degrees[interval_note_index]

        if generate_options:
            wrong_options=self.generate_interval_wrong_options(interval_note_degree, scale.scale_type.scale_degrees) #Gerar opções de reposta erradas
        else:
            wrong_options=[]

        explanation=self.generate_scale_interval_explanation(scale, interval_note)

        return IntervalScaleExercise(scale, interval_note,"Reconhecimento de intervalos em escalas musicais", interval_note_degree, wrong_options, explanation)

    def generate_scale(self, difficulty): #Gera uma escala musical de acordo com a dificuldade especificada
        tonic = random.choice(self.theory_model.TONICS) #Escolher uma nota aleatoria para ser a tónica da escala
        scale_tonic = Note(tonic.pitch, tonic.name)
        scale_type = self.select_scale_type(difficulty) #Tendo em conta as definições de dificuldade, esolher aleatoriamente um tipo de escala
        notes = self.generate_notes(scale_tonic, scale_type.scale_degrees, scale_type.note_steps) #gerar notas da escala
        return Scale(scale_tonic, scale_type, notes)

    def generate_notes(self, tonic, degrees, steps): #Gera notas musicais utilizando a descirção dos graus e de intervalos entre notas
        notes = []
        natural_pitches = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23]  # Tons das notas naturais
        natural_names = ["C", "D", "E", "F", "G", "A", "B", "C", "D", "E", "F", "G", "A","B"]  # Nomes das notas naturais

        if tonic.pitch in natural_pitches:  # Localizar o indice da nota natural associada à tonica
            index = natural_pitches.index(tonic.pitch)
        elif "#" in tonic.name:
            index = natural_pitches.index(tonic.pitch - 1)
        elif "b" in tonic.name:
            index = natural_pitches.index(tonic.pitch + 1)

        r_natural_pitches = natural_pitches[index:] + natural_pitches[:index]  # Rodar as listas para começarem na nota natural associada à tonica
        r_natural_names = natural_names[index:] + natural_names[:index]

        notes.append(tonic)  # Adicionar tónica às notas da escala

        for i in range(1,len(degrees)):  # Calcular as notas da escala com base na tónica e no tipo de escala
            pitch = notes[i - 1].pitch + steps[i - 1]  # calcular o tom da nota ao incrementar a nota anterior pelo valor do intervalo em note_steps
            degree_index = degrees[i] - 1  # Obter indice to grau da nota atual
            natural_pitch = r_natural_pitches[degree_index]  # Obter a nota natural associada ao grau da nota
            difference = pitch - natural_pitch  # Desvio do tom da nota à nota natural associada ao grau
            name = ""

            if difference == 0:  # Obter o nome correto para a nota, segundo o desvio relativamente à nota natrual
                name = r_natural_names[degree_index]
            elif difference == 1:
                name = (r_natural_names[degree_index] + "#")
            elif difference == -1:
                name = r_natural_names[degree_index] + "b"
            elif difference == 2:
                name = r_natural_names[degree_index] + "##"
            elif difference == -2:
                name = r_natural_names[degree_index] + "bb"
            notes.append(Note(pitch, name))
        return notes



    def select_scale_type(self, difficulty): #Retorna um tipo de escala aleatorio considerando as configurações de dificuldade
        possible_scales=[]
        for scale_type in self.theory_model.scale_types:
            if scale_type.name in self.scale_difficulty_settings[difficulty]:
                possible_scales.append(scale_type)
        return random.choice(possible_scales)

    def generate_interval_wrong_options(self, correct_answer_degree, scale_degrees): #Gera as opções erradas para o exercicio de intervalos
        answer_options=[]
        possible_options=list(scale_degrees)
        possible_options.remove(correct_answer_degree)

        while len(answer_options) < 3:
            answer_degree=random.choice(possible_options)
            possible_options.remove(answer_degree)
            answer_options.append(answer_degree)
        return answer_options

    def generate_scale_interval_explanation(self, scale, interval_note): #Constroi a explicação para o exercicio de intervalos
        tonic=scale.tonic.name
        scale_type=scale.scale_type.name
        intervals = "|".join( str(interval) for interval in scale.scale_type.note_steps)
        note_names = "|".join(note.name for note in scale.notes)
        degree=scale.notes.index(interval_note)+1
        explanation=(f"A escala do exercicio é a escala de {tonic} {scale_type}\n"
                     f"Uma escala {scale_type} é sempre obtida aplicando a seguinte série de intervalos a partir da tónica:\n"
                     f"{intervals}\n"
                     f"Para a tónica {tonic} a aplicação dos intervalos resulta na obtenção das notas da escala:\n"
                     f"{note_names}\n"
                     f"A nota reproduzida foi {interval_note.name} que corresponde ao {degree} grau da escala")
        return explanation

    def generate_prog_exercise(self, difficulty, generate_options=True):
        progression = self.generate_prog(difficulty)
        prog_type_name=progression.prog_type.name

        if generate_options:
            wrong_options = self.generate_prog_wrong_options(progression, difficulty)
        else:
            wrong_options = []

        explanation = self.generate_prog_explanation(progression)

        return ProgressionExercise(progression, "Reconhecimento de progressões hamónicas", prog_type_name, wrong_options, explanation)

    def generate_prog(self, difficulty): #Gera uma progressão harmónica

        prog_scale = self.generate_scale("medium")  # gerar uma escala aleatoria, "medium"-gerar apenas escalas maiores/menores
        prog_len=random.choice(self.prog_len_difficulty_settings[difficulty])
        prog_sets = self.get_prog_sets(prog_scale.scale_type.name, difficulty)
        prog_chords=[]
        prog_numerals=[]
        prog_degrees=[]
        chord_types=[]

        for i in range(prog_len):
            prog_set=random.choice(prog_sets) #Escolher um conjunto de graus de progressões

            set_numerals = list(prog_set.chord_types.keys())
            numeral = random.choice(set_numerals) #Escolher um numeral da progressão
            prog_numerals.append(numeral) #Adicionar numeral aos numerais da progressão

            chord_type_name = prog_set.chord_types[numeral] #Obter o nome do tipo de acorde

            index = set_numerals.index(numeral)
            degree = prog_set.chord_degrees[index] #Obter o grau do acorde escolhido
            degree_index=prog_scale.scale_type.scale_degrees.index(degree)
            tonic=prog_scale.notes[degree_index] #Obter a tonica do acorde correspondente ao grau da escala

            chord_tonic=Note(tonic.pitch,tonic.name)
            chord_type = self.get_chord_type(chord_type_name)  # obter o tipo do acorde
            chord_notes=self.generate_notes(chord_tonic,chord_type.chord_degrees,chord_type.note_steps) #Gerar notas do acorde
            chord=Chord(chord_tonic,chord_type,chord_notes) #Acorde da progressão

            prog_chords.append(chord) #Adicionar acorde à progressão
            prog_degrees.append(degree) #Adicionar grau à progressão
            chord_types.append(chord_type.name) #Adicionar tipo de acorde à progressão

        prog_type_name="-".join(prog_numerals) #Obter o nome do tipo de progressão
        prog_type=ChordProgType(prog_type_name,chord_types,prog_degrees) #Guardar informação sobre o tipo de progressão criado
        return ChordProg(prog_scale,prog_type,prog_chords)

    def get_prog_sets(self, mode, difficulty): #Retorna os conjuntos de progressões compativeis com o modo da escala e as definições de dificuldade
        sets=[]
        allowed=self.prog_difficulty_settings[difficulty]
        for prog_set in self.theory_model.prog_degrees:
            if prog_set.name in allowed and prog_set.mode == mode:
                sets.append(prog_set)
        return sets

    def get_chord_type(self, type_name): #retorna o tipo de acorde com o nome especificado em argumento
        for chord_type in self.theory_model.chord_types:
            if chord_type.name == type_name:
                return chord_type
        else:
            return None

    def generate_prog_wrong_options(self, progression, difficulty):  # Gera as opções erradas para os exercícios de progressões
        prog_mode=progression.scale.scale_type.name #Obter modo da progressão do exercício
        prog_type_name=progression.prog_type.name
        prog_sets = self.get_prog_sets(prog_mode, difficulty) #Obter conjuntos de graus de progressões compatives como o modo e dificuldade
        prog_len = len(progression.prog_chords)
        options = set()
        while len(options) < 3:
            prog_numerals = []
            for i in range(prog_len):
                prog_set=random.choice(prog_sets) #Escolher um conjunto de graus de progressões
                set_numerals = list(prog_set.chord_types.keys())
                numeral = random.choice(set_numerals) #Escolher um numeral da progressão
                prog_numerals.append(numeral) #Adicionar numeral aos numerais da progressão
            prog_numerals="-".join(prog_numerals)
            if prog_numerals != prog_type_name: #verificar se os numerais são diferentes da progressão do exercício (resposta correta)
                options.add(prog_numerals)

        return list(options)

    def generate_prog_explanation(self, progression): #Constroi a explicação para o exercício de progressão harmónica
        tonic=progression.scale.tonic.name
        scale_type=progression.scale.scale_type.name
        prog_name=progression.prog_type.name
        prog_type=progression.prog_type
        degrees_exp=""
        for i in range(len(prog_type.chord_types)):
            degrees_exp=degrees_exp+f"Um acorde do tipo {prog_type.chord_types[i]} no {prog_type.prog_degrees[i]}º grau da escala\n"
        chords_exp=""
        for chord in progression.prog_chords:
            chords_exp=chords_exp+f"{chord.tonic.name} {chord.chord_type.name}  "

        explanation=(f"A progressão |{prog_name}| do exercício ocorre na escala de {tonic} {scale_type}\n"
                     f"Uma progressão |{prog_name}| é contruida a partir de :\n"
                     f"{degrees_exp}\n"
                     f"Na escala de {tonic} {scale_type} esses acordes são:\n"
                     f"{chords_exp}\n")

        return explanation

    def generate_chord_exercise(self, difficulty, generate_options=True):
        chord = self.generate_chord(difficulty)
        chord_type_name=chord.chord_type.name

        if generate_options:
            wrong_options = self.generate_chord_wrong_options(chord, difficulty)
        else:
            wrong_options = []

        explanation = self.generate_chord_explanation(chord)

        return ChordExercise(chord, "Reconhecimento de acordes", chord_type_name, wrong_options, explanation)

    def generate_chord(self, difficulty):
        tonic = random.choice(self.theory_model.TONICS)  # Escolher uma nota aleatoria para ser a tónica do acorde
        chord_tonic = Note(tonic.pitch, tonic.name)
        chord_type = self.select_chord_type(difficulty)  # Tendo em conta as definições de dificuldade, esolher aleatoriamente um tipo de acorde
        notes = self.generate_notes(chord_tonic, chord_type.chord_degrees, chord_type.note_steps)  # gerar notas do acorde
        return Chord(chord_tonic, chord_type, notes)

    def select_chord_type(self, difficulty): #Retorna um tipo de acorde aleatorio considerando as configurações de dificuldade
        possible_chords=[]
        for chord_type in self.theory_model.chord_types:
            if chord_type.name in self.chord_difficulty_settings[difficulty]:
                possible_chords.append(chord_type)
        return random.choice(possible_chords)

    def generate_chord_wrong_options(self, chord, difficulty): #Gera as opcões de resposta para os exercicios de acordes
        chord_type=chord.chord_type.name
        allowed_types=self.chord_difficulty_settings[difficulty]
        option_num=min(len(allowed_types)-1, 3)
        options= set()
        while len(options) < option_num:
            option=random.choice(allowed_types)
            if option != chord_type:
                options.add(option)
        return list(options)

    def generate_chord_explanation(self, chord): #Constroi a explicação para o exercicio de acordes
        tonic=chord.tonic.name
        chord_type=chord.chord_type.name
        intervals = "|".join( str(interval) for interval in chord.chord_type.note_steps)
        note_names = "|".join(note.name for note in chord.notes)
        explanation=(f"O acorde do exercício é {tonic} {chord_type}\n"
                     f"Uma acorde {chord_type} é construido aplicando a seguinte série de intervalos a partir da tónica:\n"
                     f"{intervals}\n"
                     f"Para a tónica {tonic} a aplicação dos intervalos resulta na obtenção das notas do acorde:\n"
                     f"{note_names}\n")
        return explanation






