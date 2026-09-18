import random

from src.AudioEngine.audio_engine import AudioEngine
from src.ExerciseGenerator.exercise_generator import ExerciseGenerator
from src.MusicTheoryModel.music_theory_model import MusicTheoryModel

class ExerciseSession: #Sessão para realização de um conjunto de exercícios
    def __init__(self, exercises, audio_engine):
        self.audio_engine=audio_engine
        self.exercises=exercises #Exercícios da sessão
        self.current_index=0 #Índice do exercício atual
        self.exercise_answered=False #Regista se o exercício atual já foi respondido
        self.correct_count=0 #Contagem de respostas respondidas corretamente
        self.accuracy=0 #Precisão nas respostas do conjunto de exercícios
        self.evaluation="" #Nota qualificativa do desempenho

    def current_exercise(self): #Retorna o exercício atual
        return self.exercises[self.current_index]

    def next_exercise(self): #Avança a sessão para o próximo exercício
        self.current_index+=1
        self.exercise_answered=False

    def is_finished(self): #Retorna um bool para indicar se a sessão chegou ao fim
        return self.current_index+1 == len(self.exercises) and self.exercise_answered

    def audio_playing(self): #Verifica se existe áudio em reprodução (reprodução assíncrona)
        return self.audio_engine.is_playing()

    def exercise_title(self): #Retorna o título do exercício atual
        return self.current_exercise().title

    def exercise_explanation(self): #Retorna a explicação do exercício
        return self.current_exercise().explanation

    def exercise_answer_options(self): #Retorna as opções de resposta do exercício
        options=self.current_exercise().wrong_options.copy()
        options.append(self.current_exercise().correct_answer)
        random.shuffle(options)
        return options

    def validate_answer(self, answer): #Valida a resposta selecionada
        if not self.exercise_answered:
            self.exercise_answered=True
            if self.answer_is_correct(answer):
                self.correct_count+=1

    def answer_is_correct(self, answer): #Retorna um bool para indicar se a resposta selecionada está correta
        return answer == self.current_exercise().correct_answer

    def set_result_stats(self): #Calcula e atualiza as estatisticas de desempenho
        self.accuracy=(self.correct_count / len(self.exercises)) * 100
        if  self.accuracy <= 25:
            self.evaluation="Fraco"
        elif self.accuracy <= 50:
            self.evaluation="Insuficiente"
        elif self.accuracy<= 75:
            self.evaluation="Suficiente"
        elif self.accuracy <= 100:
            self.evaluation="Bom"



class IntervalScaleSession(ExerciseSession): #Sessão para realização de um conjunto de exercícios
    def __init__(self,exercises, audio_engine):
        super().__init__(exercises, audio_engine)
        self.exercise_type = "interval_scale"


    def play_exercise_tonic(self): #Reproduzir a tónica do exercício

        note=self.exercises[self.current_index].scale.tonic
        self.audio_engine.play_note(note,1,3)

    def play_exercise_interval_note(self): #Reproduzir a nota musical do intervalo
        note = self.exercises[self.current_index].interval_note
        self.audio_engine.play_note(note,1,3)

    def play_exercise_interval(self): #Reproduzir o intervalo (tónica e nota do intervalo)
        t_note=self.exercises[self.current_index].scale.tonic
        i_note=self.exercises[self.current_index].interval_note
        notes=[t_note,i_note]
        self.audio_engine.play_note_sequence(notes,1,3)

    def current_exercise_scale_info(self): #Retorna o nome da escala
        exercise=self.exercises[self.current_index]
        return f"Escala {exercise.scale.tonic.name} {exercise.scale.scale_type.name}"




class ExerciseManager: #Gestor de exercícios

    def __init__(self):
        self.theory_model=MusicTheoryModel()
        self.exercise_generator=ExerciseGenerator(self.theory_model)
        self.audio_engine=AudioEngine()
        self.exercise_session=None


    def create_exercise_session(self, selected_exercise,selected_difficulty, selected_exercise_num, selected_mode):
        generator=self.exercise_generator
        exercises=[]
        if selected_mode == "gui": generate_options=True
        else: generate_options=False
        match selected_exercise:
            case "interval_scale":
                for i in range(selected_exercise_num): #Gerar o número de exercícios pretendidos de acordo com as configurações selecionada
                    exercises.append(generator.generate_scale_interval_exercise(selected_difficulty,generate_options))
                self.exercise_session=IntervalScaleSession(exercises, self.audio_engine) #Criar sessão com os exercícios gerados


