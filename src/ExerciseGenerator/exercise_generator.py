
from src.MusicTheoryModel.music_theory_model import *
import random

class Exercise: #Formato de um exercicio
    def __init__(self, title, correct_answer, wrong_answers, explanation):
        self.title = title
        self.wrong_options = wrong_answers
        self.correct_answer = correct_answer
        self.explanation = explanation

class IntervalScaleExercise(Exercise): #Exercicio de reconhecimento de intervalos no contexto de uma escala

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


class Scale: #Escala musical
    def __init__(self, tonic, scale_type, notes):
        self.tonic=tonic
        self.scale_type=scale_type
        self.notes=notes


class ExerciseGenerator: #Gerador de exercicios
    scale_difficulty_settings = {"easy": ("Major"), "medium": ("Major", "Minor"), "hard" :("Major", "Minor", "Major Pentatonic", "Minor Pentatonic", "Mixolydian", "Dorian")} #Definições de dificuldade relativas ao tipo de escala
    interval_difficulty_settings= {"easy": 3, "medium": 2, "hard" :1} #Definições de dificuldade relativas aos intervalos apresentados como opções de resposta
    def __init__(self, theory_model):
        self.theory_model=theory_model #Modelo de teoria que o gerador utiliza

    def generate_scale_interval_exercise(self, difficulty): #Gera um exercicio de reconhecimento de intervalos no contexto de uma escala
        scale=self.generate_scale(difficulty) #Gerar uma escala
        interval_note=random.choice(scale.notes[1:]) #Escolher uma nota da escala para obter o intervalo do exercicio
        interval_note_degree=scale.notes.index(interval_note)+1 #Grau da nota do intervalo
        wrong_options=self.generate_interval_wrong_options(interval_note_degree, len(scale.notes), difficulty) #Gerar opções de reposta erradas
        explanation=self.generate_scale_interval_explanation(scale, interval_note)

        return IntervalScaleExercise(scale, interval_note,"Reconhecimento de intervalos em escalas musicais", interval_note_degree, wrong_options, explanation)

    def generate_scale(self, difficulty): #Gera uma escala musical
        tonic = random.choice(self.theory_model.TONICS) #Escolher uma nota aleatoria para ser a tonica da escala
        scale_type = self.select_scale_type(difficulty) #Tendo em conta as definições de dificuldade, esolher aleatoriamente um tipo de escala
        notes = []
        natural_pitches = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23] #Tons das notas naturais
        natural_names=["C","D","E","F","G","A","B","C","D","E","F","G","A","B"] #Nomes das notas naturais

        if tonic.pitch in natural_pitches: #Localizar o indice da nota natural associada à tonica
            index = natural_pitches.index(tonic.pitch)
        elif "#" in tonic.name:
            index=natural_pitches.index(tonic.pitch-1)
        elif "b" in tonic.name:
            index = natural_pitches.index(tonic.pitch + 1)

        r_natural_pitches = natural_pitches[index:] + natural_pitches[:index] #Rodar as listas para começarem na nota natural associada à tonica
        r_natural_names=natural_names[index:]+natural_names[:index]

        notes.append(tonic) #Adicionar tonica às notas da escala

        for i in range(1,len(scale_type.scale_degrees)): #Calcular as notas da escala com base na tónica e tipo de escala
            pitch=notes[i-1].pitch+scale_type.note_steps[i-1] #calcular o tom da nota ao incrementar a nota anterior pelo valor do intervalo em note_steps
            degree_index=scale_type.scale_degrees[i]-1 #Obter indice to grau da nota atual
            natural_pitch=r_natural_pitches[degree_index] #Obter a nota natural associada ao grau da nota
            difference=pitch - natural_pitch #Desvio do tom da nota à nota natural associada ao grau
            name=""

            if difference == 0: #Obter o nome correto para a nota segundo o desvio relativamente à nota natrual
                 name=r_natural_names[degree_index]
            elif difference == 1:
                name=(r_natural_names[degree_index]+"#")
            elif difference == -1:
                name=r_natural_names[degree_index]+"b"
            elif difference == 2:
                 name=r_natural_names[degree_index]+"##"
            elif difference == -2:
                name=r_natural_names[degree_index]+"bb"
            notes.append(Note(pitch,name))

        return Scale(tonic, scale_type, notes)



    def select_scale_type(self, difficulty): #Retorna um tipo de escala aleatorio considerando as configurações de dificuldade
        possible_scales=[]
        for scale_type in self.theory_model.scale_types:
            if scale_type.name in self.scale_difficulty_settings[difficulty]:
                possible_scales.append(scale_type)
        return random.choice(possible_scales)

    def generate_interval_wrong_options(self, correct_answer_degree, scale_degrees, difficulty): #Gera as opções erradas para o exercicio de intervalos de acordo com as definições de dificuldade
        min_range=self.interval_difficulty_settings[difficulty]

        left_item=correct_answer_degree-min_range
        right_item=correct_answer_degree+min_range
        answer_options=[]

        possible_options=list(range(1,scale_degrees+1))
        possible_options.remove(correct_answer_degree)

        while left_item>=1 or right_item <=scale_degrees:
            if left_item>=1:
                answer_options.append(left_item)
                possible_options.remove(left_item)
                left_item=left_item-min_range

            if right_item<=scale_degrees:
                answer_options.append(right_item)
                possible_options.remove(right_item)
                right_item=right_item+min_range


        while len(answer_options) != 3:
            if len(answer_options)<3:
                option=random.choice(possible_options)
                answer_options.append(option)
                possible_options.remove(option)
            else:
                option = random.choice(answer_options)
                answer_options.remove(option)

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




