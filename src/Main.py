import time

from PySide6 import QtWidgets


from src.ExerciseManager.exercise_manager import ExerciseManager
from src.Gui.gui import MainWindow
import sys

from src.MIDIEngine.midi_engine import MidiListener


class Main:
    def __init__(self):

        self.exercise_manager = ExerciseManager() #Gestor de exercícios
        self.midi_listener = MidiListener()

        #Inicializar interface gráfica
        self.app = QtWidgets.QApplication([])
        self.window = MainWindow()
        self.window.resize(800, 600)
        self.window.show()

        #Ecrãs da interface
        self.config_screen = self.window.config_page
        self.i_s_screen = self.window.int_scale_exercise_page
        self.p_screen = self.window.prog_exercise_page
        self.c_screen = self.window.chord_exercise_page
        self.r_screen = self.window.rythm_exercise_page
        self.explain_screen = self.window.explanation_page
        self.eval_screen = self.window.evaluation_page

        #Conectar os eventos da interface às ações a tomar
        self.config_screen.exercise_configured.subscribe(self.start_exercises)
        self.i_s_screen.tonic_playback_requested.subscribe(self.play_i_s_tonic)
        self.i_s_screen.interval_note_playback_requested.subscribe(self.play_i_s_interval_note)
        self.i_s_screen.multiple_choice.answer_submited.subscribe(self.process_i_s_answer)
        self.i_s_screen.explanation_requested.subscribe(self.show_explanation)
        self.explain_screen.next_exercise_requested.subscribe(self.next_exercise)
        self.eval_screen.eval_continue_pressed.subscribe(self.show_menu)
        self.p_screen.prog_playback_requested.subscribe(self.play_p_rogression)
        self.p_screen.multiple_choice.answer_submited.subscribe(self.process_p_answer)
        self.p_screen.explanation_requested.subscribe(self.show_explanation)
        self.c_screen.chord_playback_requested.subscribe(self.play_c_chord)
        self.c_screen.multiple_choice.answer_submited.subscribe(self.process_c_answer)
        self.c_screen.explanation_requested.subscribe(self.show_explanation)
        self.r_screen.rythm_plyback_requested.subscribe(self.play_r_rythm)
        self.r_screen.answer_button_pressed.subscribe(self.process_r_input)
        self.r_screen.explanation_requested.subscribe(self.show_explanation)



    def show_menu(self): #Mostra menu de seleção de exercícios
        self.window.show_menu()

    def start_exercises(self, selected_exercise, selected_difficulty, selected_exercise_num, selected_mode):
        self.exercise_manager.create_exercise_session(selected_exercise, selected_difficulty, selected_exercise_num, selected_mode) #Criar sessão com as configurações selecionadas na interface
        self.show_exercise(selected_exercise) #Exibir exercício na interface

    def next_exercise(self):
        session = self.exercise_manager.exercise_session
        exercise_type=session.exercise_type #Avançar para o próximo exercício
        if not session.is_finished():
            session.next_exercise()
            self.show_exercise(exercise_type) #Se a sessão não terminou, apresentar o próximo exercício
        else:
            self.on_session_end() #Caso contrário, apresentar avaliação do desempenho

    def show_exercise(self, selected_exercise): #Mostra o exercício na interface
        match selected_exercise:
            case "interval_scale":
                self.show_i_s_exercise()
            case "harmonic_prog":
                self.show_p_exercise()
            case "chord":
                self.show_c_exercise()
            case "rythm":
                self.show_r_exercise()

    def show_i_s_exercise(self): #Mostra um exercício de reconhecimento de intervalos em escalas na interface
        session = self.exercise_manager.exercise_session
        scale_info = session.current_exercise_scale_info()
        if session.mode == "gui":
            options = session.exercise_answer_options()
            self.window.show_mc_interval_scale_page(scale_info, options)
        elif session.mode == "midi":
            self.midi_listener.listen_for_key()
            self.window.show_midi_interval_scale_page(scale_info, 2)
            self.midi_listener.midi_key_pressed.subscribe(self.on_i_s_midi_input)

    def show_p_exercise(self): #Mostra um exercício de reconhecimento de progressões harmonicas na interface
        session = self.exercise_manager.exercise_session
        prog_info = session.current_exercise_prog_info()
        options = session.exercise_answer_options()
        self.window.show_prog_page(prog_info, options)

    def show_c_exercise(self):  # Mostra um exercício de reconhecimento de acordes na interface
        session = self.exercise_manager.exercise_session
        chord_info = session.current_exercise_chord_info()
        options = session.exercise_answer_options()
        self.window.show_chord_page(chord_info, options)

    def show_r_exercise(self):
        session = self.exercise_manager.exercise_session
        print(session.current_exercise().explanation)
        self.window.show_rythm_page()

    def show_explanation(self):
        session = self.exercise_manager.exercise_session
        explanation=session.exercise_explanation()
        self.window.show_explanation_page(explanation)

    def process_i_s_answer(self, answer): #valida resposta e mostra feedback
        session = self.exercise_manager.exercise_session
        session.validate_answer(answer)
        if session.answer_is_correct(answer):
            feedback="Certo!"
        else:
            feedback="Errado!"
        self.i_s_screen.set_feedback(feedback)
        self.i_s_screen.show_feedback()

    def process_p_answer(self, answer): #valida resposta e mostra feedback
        session = self.exercise_manager.exercise_session
        session.validate_answer(answer)
        if session.answer_is_correct(answer):
            feedback="Certo!"
        else:
            feedback="Errado!"
        self.p_screen.set_feedback(feedback)
        self.p_screen.show_feedback()

    def process_c_answer(self, answer): #valida resposta e mostra feedback
        session = self.exercise_manager.exercise_session
        session.validate_answer(answer)
        if session.answer_is_correct(answer):
            feedback="Certo!"
        else:
            feedback="Errado!"
        self.c_screen.set_feedback(feedback)
        self.c_screen.show_feedback()

    def process_r_input(self):
        current_time=time.perf_counter()
        session=self.exercise_manager.exercise_session
        session.play_input_sound()
        session.validate_input(current_time)
        if session.exercise_answered:
            feedback=session.get_last_rating_feedback()
            self.r_screen.set_feedback(feedback)


    def play_i_s_tonic(self):
        session = self.exercise_manager.exercise_session
        session.play_exercise_tonic()

    def play_i_s_interval_note(self):
        session = self.exercise_manager.exercise_session
        session.play_exercise_interval_note()

    def play_p_rogression(self):
        session = self.exercise_manager.exercise_session
        session.play_exercise_prog()

    def play_c_chord(self):
        session = self.exercise_manager.exercise_session
        session.play_exercise_chord()

    def play_r_rythm(self):
        session = self.exercise_manager.exercise_session
        session.play_exercise_rythm()

    def on_session_end(self):
        session = self.exercise_manager.exercise_session
        if session.mode == "midi":
            self.midi_listener.stop_listening()
        self.show_eval()


    def show_eval(self):
        session = self.exercise_manager.exercise_session
        session.set_result_stats()
        results=session.get_result_stats()
        self.window.show_evaluation_page(results)

    def on_i_s_midi_input(self, midi_key):
        session = self.exercise_manager.exercise_session
        session.receive_input(midi_key)
        self.i_s_screen.set_feedback(session.last_feedback)
        self.i_s_screen.midi_feedback.set_feedback(session.get_input_feedback())
        if session.exercise_answered:
            self.midi_listener.midi_key_pressed.unsubscribe(self.on_i_s_midi_input)




main=Main()
sys.exit(main.app.exec())


