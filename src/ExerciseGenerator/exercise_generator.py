
from src.MusicTheoryModel.music_theory_model import MusicTheoryModel
import random

class Exercise: #Formato de um exercicio
    def __init__(self, title, correct_answer, wrong_answers):
        self.title = title
        self.wrong_options = wrong_answers
        self.correct_answer = correct_answer
        self.explanation = None

class IntervalScaleExercise(Exercise): #Exercicio de reconhecimento de intervalos no contexto de uma escala

    def __init__(self, title, correct_answer, wrong_answers, scale):
        super().__init__(title, correct_answer, wrong_answers)
        self.scale=scale


class Scale: #Escala musical
    def __init__(self, tonic, scale_type, notes):
        self.tonic=tonic
        self.scale_type=scale_type
        self.notes=notes
        self.note_names=None
        self.scale_name=None

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
        return IntervalScaleExercise("Titulo Placeholder", interval_note_degree, wrong_options, scale)

    def generate_scale(self, difficulty): #Gera uma escala musical
        tonic = random.choice(self.theory_model.TONICS) #Escolher uma nota aleatoria para ser a tonica da escala
        scale_type = self.select_scale_type(difficulty) #Esolher aleatoriamente um tipo de escala
        notes = []
        for offset in scale_type.note_offsets: #Calcular as notas da escala com base na tónica e tipo de escala obtidos
            notes.append(tonic + offset)
        # note_names = self.build_note_names(notes, scale_type.scale_degrees)
        # scale_name = note_names[0] + scale_type.name
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




