
from src.MusicTheoryModel.music_theory_model import Scale, Note, Chord, ChordProg, ChordProgType, Rythm

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

class RythmExercise:
    def __init__(self, title, rythm, attack_times,explanation):
        self.title=title
        self.rythm=rythm
        self.attack_times=attack_times
        self.explanation=explanation


class ExerciseGenerator: #Gerador de exercicios
    scale_difficulty_settings = {"easy": ("Major",), "medium": ("Major", "Minor"), "hard" :("Major", "Minor", "Major Pentatonic", "Minor Pentatonic", "Mixolydian", "Dorian")} #Definições de dificuldade relativas ao tipo de escala
    prog_difficulty_settings = {"easy":("MajorDiatonics","MinorDiatonics"),
                                "medium":("MajorDiatonics","MinorDiatonics","Major7thDiatonics","Minor7thDiatonics"),
                                "hard":("MajorDiatonics","MinorDiatonics","Major7thDiatonics","Minor7thDiatonics","MajorSus2","MinorSus2","MajorSus4","MinorSus4")}
    prog_len_difficulty_settings = {"easy":(2,),"medium":(2,3,4),"hard": (4,5,6)}
    chord_difficulty_settings ={"easy":("Major","Minor"), "medium":("Major","Minor","Major7","Minor7","7"),"hard":("Major","Minor","Major7","Minor7","7","Diminished","Diminished7","Halfdiminished7","Sus2","Sus4")}
    rythm_cmp_difficulty_settings={"easy":("4/4",),"medium":("4/4","3/4","2/4"),"hard":("4/4","3/4","2/4","5/4","7/4")}
    rythm_len_difficulty_settings={"easy":1, "medium":2, "hard":3}
    rythm_unit_difficulty_settings={"easy":("Half","Quarter"),"medium":("Whole","Half","Quarter","Eighth"),"hard":("Whole","Half","Quarter","Eighth","Sixteenth")}

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

    def steps_to_txt(self, note_steps):
        txt=[]
        for step in note_steps:
            if step == 1:
                txt.append("um semitom")
            elif step == 2:
                txt.append("um tom")
            else:
                txt.append(f"{step} semitons")
        if len(txt)==1:
            return txt[0]
        else:
            return ", ".join(txt[:-1]) + " e " + txt[-1]

    def generate_scale_interval_explanation(self, scale, interval_note): #Constroi a explicação para o exercicio de intervalos
        tonic=scale.tonic.name
        type=scale.scale_type.description.lower()
        steps=self.steps_to_txt(scale.scale_type.note_steps)
        notes=[]
        for i in range(len(scale.notes)):
            notes.append(f"{scale.notes[i].name} ({scale.scale_type.scale_degrees[i]}º)")
        if len(notes)==1:
            notes_txt = notes[0]
        else:
            notes_txt=", ".join(notes[:-1]) + " e " + notes[-1]
        d_index=scale.notes.index(interval_note)
        degree=scale.scale_type.scale_degrees[d_index]

        explanation=(f"A escala do exercicio é a de {tonic} {type}\n"
                     f"A escala {type} é construida aplicando a seguinte sucessão de intervalos a partir da tónica:\n"
                     f"{steps}\n"
                     f"Para a tónica {tonic}, a aplicação dos intervalos resulta na obtenção das seguintes notas da escala:\n"
                     f"{notes_txt}\n"
                     f"A nota reproduzida foi {interval_note.name}, que corresponde ao {degree} grau diatónico")
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
        scale_type=progression.scale.scale_type.description
        prog_name=progression.prog_type.name
        prog_numerals=prog_name.split("-")
        scale=progression.scale
        chords=progression.prog_chords

        notes = []
        for i in range(len(scale.notes)):
            notes.append(f"{scale.notes[i].name} ({scale.scale_type.scale_degrees[i]}º)")
        if len(notes) == 1:
            notes_txt = notes[0]
        else:
            notes_txt = ", ".join(notes[:-1]) + " e " + notes[-1]
        chord_txt=[]
        for i in range(len(prog_numerals)):
            numeral = prog_numerals[i]
            degree=progression.prog_type.prog_degrees[i]
            chord_type=chords[i].chord_type.description.lower()
            chord_name=f"{chords[i].tonic.name}{chords[i].chord_type.symbol}"
            chord_txt.append(f"{numeral}: No {degree}º grau constrói um acorde {chord_type}, resultando no acorde {chord_name}\n")
        chord_txt="".join(chord_txt)

        explanation = (f"A progressão do exercício é {prog_name} e ocorre na tonalidade de {tonic} {scale_type}, cujas notas são:\n"
                       f"{notes_txt}.\n"
                       f"Cada numeral indica um grau dessa escala e a qualidade do acode que aí se forma: \n"
                       f"{chord_txt}\n")

        return explanation

    def generate_chord_exercise(self, difficulty, generate_options=True):
        chord = self.generate_chord(difficulty)
        tonic=chord.tonic.name
        chord_type_symbol=chord.chord_type.symbol
        correct_answer=tonic+chord_type_symbol

        if generate_options:
            wrong_options = self.generate_chord_wrong_options(chord, difficulty)
        else:
            wrong_options = []

        explanation = self.generate_chord_explanation(chord)

        return ChordExercise(chord, "Reconhecimento de acordes", correct_answer, wrong_options, explanation)

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
        chord_type=chord.chord_type
        allowed_types=self.chord_difficulty_settings[difficulty]
        option_num=min(len(allowed_types)-1, 3)
        options= set()
        while len(options) < option_num:
            option_type=self.get_chord_type(random.choice(allowed_types))
            if option_type != chord_type:
                option=chord.tonic.name+option_type.symbol
                options.add(option)
        return list(options)

    def generate_chord_explanation(self, chord): #Constroi a explicação para o exercicio de acordes
        tonic=chord.tonic.name
        chord_type=chord.chord_type.description
        symbol=chord.chord_type.symbol
        steps=self.steps_to_txt(chord.chord_type.note_steps)
        notes = []
        for i in range(len(chord.notes)):
            notes.append(f"{chord.notes[i].name} ({chord.chord_type.chord_degrees[i]}º)")
        if len(notes) == 1:
            notes_txt = notes[0]
        else:
            notes_txt = ", ".join(notes[:-1]) + " e " + notes[-1]

        explanation = (f"O acorde do exercício é {tonic}{symbol} ({chord_type})\n"
                       f"Um acorde {chord_type} é construido aplicando a seguinte sucessão de intervalos a partir da tónica:\n"
                       f"{steps}\n"
                       f"Para a tónica {tonic}, a aplicação dos intervalos resulta na obtenção das seguintes notas do acorde:\n"
                       f"{notes_txt}\n")
        return explanation

    def generate_rythm_exercise(self, difficulty):
        rythm = self.generate_rythm(difficulty)
        attack_times=[0]
        for measure in rythm.measures:
            for unit in measure:
                attack_times.append(attack_times[-1]+unit.duration)
        attack_times.pop()

        explanation = self.generate_rythm_explanation(rythm)

        return RythmExercise("Reconhecimento e execução de ritmos", rythm, attack_times,explanation)

    def generate_rythm(self, difficulty): #Gera um ritmo em função do nível de dificuldade
        compass= random.choice(self.rythm_cmp_difficulty_settings[difficulty]) #Escolher uma fórmula de compasso
        measure_num= self.rythm_len_difficulty_settings[difficulty] #Obter o número de compassos do rítmo
        compass_nums=compass.split("/")
        compass_n=int(compass_nums[0])
        compass_d=int(compass_nums[1])
        measure_len=compass_n/compass_d #Calcular duração de cada compasso
        measures=[]
        duration_tolerance=1e-9 #margem de erro para as operações realizadas
        while len(measures)<measure_num: #Até preencher o número de compassos do rítmo
            measure = self.generate_measure(difficulty, measure_len, duration_tolerance) #gerar um compasso completo
            measures.append(measure)
        return Rythm(compass,measures)

    def generate_measure(self, difficulty, measure_len, duration_tolerance): #gera um compasso completo
        max_tries = 40 #segurança para evitar que a aplicação deixe de responder, caso ocorra uma situação inesperada emite um erro
        for i in range(max_tries):
            units=[]
            remaining=measure_len
            allowed=self.get_rythm_units(difficulty, remaining) #obter unidades ritmicas compativeis com a dificuldade e duração de compasso restante
            while remaining > duration_tolerance and allowed: #adicionar unidades até o compasso preencher ou até que não existam unidades compatíveis
                unit = random.choice(allowed)
                units.append(unit)
                remaining -= unit.duration
                allowed=self.get_rythm_units(difficulty, remaining)
            if remaining <= duration_tolerance: #retornar unidades caso o compasso esteja preenchido
                return units
        raise RuntimeError("Não foi possível preencher um compasso completo")



    def get_rythm_units(self, difficulty, measure_left): #Retorna as unidades rítmicas compativeis com a dificuldade e com a duração restante do compasso
        allowed_units=[]
        for rythm_unit in self.theory_model.rythm_units:
            if rythm_unit.name in self.rythm_unit_difficulty_settings[difficulty] and rythm_unit.duration <= measure_left:
                allowed_units.append(rythm_unit)
        return allowed_units

    def generate_rythm_explanation(self, rythm):
        compass=rythm.compass
        measure_n=len(rythm.measures)
        measure_ex = ""
        for i, measure in enumerate(rythm.measures, start=1):
            measure_ex+=f"-⮞ No {i}º compasso:  "
            for unit in measure:
                measure_ex+=f"Uma {unit.description} {unit.symbol}; "
            measure_ex+="\n"
        explanation = f"O ritmo está na fórmula {compass} e ocupa {measure_n}"
        if measure_n == 1:
            explanation+=" compasso.\n"
        else:
            explanation+=" compassos.\n"
        explanation+=f"O ritmo reproduzido é composto por:\n {measure_ex}\n"
        return explanation



