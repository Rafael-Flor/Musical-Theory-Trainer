import random
import time

from src.AudioEngine.audio_engine import AudioEngine
from src.Events import Event
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

class MultipleCSession(ExerciseSession): #Sessões para exercícios de escolha múltipla

    def __init__(self,exercises, audio_engine):
        super().__init__(exercises, audio_engine)
        self.mode="gui"

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

    def get_result_stats(self):
        return [("Numero de exercícios corretos", self.correct_count),("Precisão", self.accuracy),("Avaliação",self.evaluation)]

class IntervalScaleMethods: #Métodos para os exercícios de reconhecimento de intervalos em escalas

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

class IntervalScaleSession(MultipleCSession, IntervalScaleMethods): #Sessão para realização de um conjunto de exercícios
    def __init__(self,exercises, audio_engine):
        super().__init__(exercises, audio_engine)
        self.audio_engine.load_piano()
        self.exercise_type = "interval_scale"

class ProgressionSession(MultipleCSession): #Sessão para realização de exercícios de progressões
    def __init__(self,exercises, audio_engine):
        super().__init__(exercises, audio_engine)
        self.audio_engine.load_piano()
        self.exercise_type="harmonic_prog"

    def play_exercise_prog(self): #Reproduz a progressão do exercício
        chords=self.current_exercise().progression.prog_chords
        self.audio_engine.play_chord_sequence(chords,2,3)

    def current_exercise_prog_info(self): #Obtem informação sobre a progressão (tonalidade)
        exercise=self.current_exercise()
        prog=exercise.progression
        return f"Tonalidade {prog.scale.tonic.name} {prog.scale.scale_type.name}"

class ChordSession(MultipleCSession): #Sessão para realização de exercícios de acordes
    def __init__(self,exercises, audio_engine):
        super().__init__(exercises, audio_engine)
        self.audio_engine.load_piano()
        self.exercise_type="chord"

    def play_exercise_chord(self): #Reproduz o acorde do exercício
        chord=self.current_exercise().chord
        self.audio_engine.play_chord(chord,2,3)

    def current_exercise_chord_info(self): #Obtem informação sobre o acorde (tonica)
        exercise=self.current_exercise()
        chord=exercise.chord
        return f"Tónica {chord.tonic.name}"

class RythmSession(ExerciseSession): #Sessão para realizar exercícios de ritmo
    def __init__(self,exercises, audio_engine):
        super().__init__(exercises, audio_engine)
        self.audio_engine.load_drums()
        self.exercise_type="rythm"
        self.exercise_accuracies=[]
        self.answer_ratings=[]
        self.input_count=0
        self.start_time=0
        self.rythm_speed=0.5

    def play_exercise_rythm(self): #Reproduz o ritmo do exercício
        rythm=self.current_exercise().rythm
        self.audio_engine.play_rythm(rythm, self.rythm_speed)

    def play_input_sound(self):
        self.audio_engine.play_rythm_tap()

    def validate_input(self, time): #Valida um input de resposta
        if not self.exercise_answered:
            if self.input_count==0: #Definir o momento do 1º input de resposta como o inicio do ritmo introduzido
                self.start_time=time
                self.input_count+=1
            else:
                attack_count = 0
                for measure in self.current_exercise().rythm.measures:  # Contabilizar o número de ataques no ritmo
                    for unit in measure:
                        attack_count += 1
                target=self.current_exercise().attack_times[self.input_count]/self.rythm_speed+self.start_time #Tempo alvo do próximo ataque do ritmo
                error=abs(target-time)*100 #Erro em ms do input em relação ao tempo alvo
                print(error)
                if error <= 25: #Classificar o input com base no erro
                    self.exercise_accuracies.append(3)
                elif error <= 50:
                    self.exercise_accuracies.append(2)
                else:
                    self.exercise_accuracies.append(1)
                print(self.exercise_accuracies[-1])
                self.input_count+=1
                if self.input_count >= attack_count: #Verificar se o ritmo introduzido terminou
                    self.input_count=0
                    self.exercise_answered=True
                    self.set_answer_accuracy()

    def get_last_rating_feedback(self):
        rating=self.answer_ratings[-1]
        print(rating)
        if rating < 1.5:
            return "Fraco"
        elif rating < 2.5:
            return "Suficiente"
        else:
            return "Bom"

    def set_answer_accuracy(self): #Adiciona a média do desempenho no exercício à lista de avaliações da sessão
        self.answer_ratings.append(sum(self.exercise_accuracies)/(len(self.exercise_accuracies)))

    def set_result_stats(self): #Atualiza as estatisticas de desempenho
        self.accuracy=sum(self.answer_ratings)/len(self.answer_ratings)
        if self.accuracy < 1.5:
            self.evaluation = "Fraco"
        elif self.accuracy < 2.5:
            self.evaluation = "Suficiente"
        else:
            self.evaluation = "Bom"

    def next_exercise(self): #Avana para o próximo exercício da sessão
        self.current_index+=1
        self.exercise_answered=False
        self.exercise_accuracies=[]
        self.input_count=0

    def get_result_stats(self):
        return [("Precisão", self.accuracy/3),("Avaliação",self.evaluation)]

class ExerciseManager: #Gestor de exercícios

    def __init__(self):
        self.theory_model=MusicTheoryModel()
        self.exercise_generator=ExerciseGenerator(self.theory_model)
        self.audio_engine=AudioEngine()
        self.exercise_session=None


    def create_exercise_session(self, selected_exercise,selected_difficulty, selected_exercise_num, selected_mode):
        generator=self.exercise_generator
        exercises=[]
        if selected_mode == "gui":
            generate_options=True
            match selected_exercise:
                case "interval_scale":
                    for i in range(selected_exercise_num): #Gerar o número de exercícios pretendidos de acordo com as configurações selecionada
                        exercises.append(generator.generate_scale_interval_exercise(selected_difficulty,generate_options))
                    self.exercise_session=IntervalScaleSession(exercises, self.audio_engine) #Criar sessão com os exercícios gerados
                case "harmonic_prog":
                    for i in range(selected_exercise_num):
                        exercises.append(generator.generate_prog_exercise(selected_difficulty, generate_options))
                    self.exercise_session=ProgressionSession(exercises, self.audio_engine)
                case "chord":
                    for i in range(selected_exercise_num):
                        exercises.append(generator.generate_chord_exercise(selected_difficulty, generate_options))
                    self.exercise_session = ChordSession(exercises, self.audio_engine)
                case "rythm":
                    for i in range(selected_exercise_num):
                        exercises.append(generator.generate_rythm_exercise(selected_difficulty))
                    self.exercise_session = RythmSession(exercises, self.audio_engine)
