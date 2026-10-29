from src.AudioEngine.audio_engine import AudioEngine
from src.ExerciseGenerator.exercise_generator import ExerciseGenerator
from src.ExerciseManager.catalog import get_exercise
from src.ExerciseManager.sessions import IntervalScaleSession, MidiIntervalSclSession, ProgressionSession, ChordSession, \
    MidiChordSession, RythmSession
from src.MusicTheoryModel.music_theory_model import MusicTheoryModel



class ExerciseManager: #Gestor de exercícios

    GENERATORS= { #Chamadas a utilizar para gerar cada tipo de exercício
        "interval_scale": lambda generator, difficulty, generate_options: generator.generate_scale_interval_exercise(difficulty, generate_options),
        "harmonic_prog": lambda generator, difficulty, generate_options: generator.generate_prog_exercise(difficulty, generate_options),
        "chord": lambda generator, difficulty, generate_options: generator.generate_chord_exercise(difficulty,generate_options),
        "rythm": lambda generator, difficulty, generate_options: generator.generate_rythm_exercise(difficulty),
    }

    SESSIONS = { #Sessões a utilizar para realizar um exercício num determinado modo
        ("interval_scale","gui"): IntervalScaleSession,
        ("interval_scale", "midi"): MidiIntervalSclSession,
        ("harmonic_prog", "gui"): ProgressionSession,
        ("chord", "gui"): ChordSession,
        ("chord", "midi"): MidiChordSession,
        ("rythm", "gui"): RythmSession,
    }

    def __init__(self):
        self.theory_model=MusicTheoryModel()
        self.exercise_generator=ExerciseGenerator(self.theory_model)
        self.audio_engine=AudioEngine()
        self.exercise_session=None


    def create_exercise_session(self, selected_exercise,selected_difficulty, selected_exercise_num, selected_mode):
        generator=self.exercise_generator
        exercises=[]
        ex_info=get_exercise(selected_exercise) #Obter informação do ex. a partir do catalogo
        if selected_mode not in ex_info["modes"]: #Veriicar se o modo escolhido é compativel com o exercício selecionado
            raise ValueError(f"Modo '{selected_mode}' não disponivel para o exercício escolhido: '{selected_exercise}'")
        if selected_mode == "gui": #geração de opções de resposta apenas relevante para o modo gui
            generate_options=True
        else:
            generate_options=False

        generate_ex=self.GENERATORS[ex_info["id"]] #Obter a chamada adequada para gerar o tipo de exercício especificado

        for i in range(selected_exercise_num): #gerar o número de exercícios especificado
            exercises.append(generate_ex(generator, selected_difficulty, generate_options))

        session_class=self.SESSIONS[ex_info["id"], selected_mode] #obter a classe da sessão adequada para realizar os exercícios
        self.exercise_session=session_class(exercises, self.audio_engine) #criar sessão

