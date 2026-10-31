import time

from PySide6 import QtWidgets

from src.ExerciseManager.catalog import EXERCISES
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
        self.window.setFixedSize(900, 700)
        self.window.main_menu.set_main_menu(EXERCISES)
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
        self.config_screen.menu_requested.subscribe(self.show_menu)
        self.i_s_screen.tonic_playback_requested.subscribe(self.play_i_s_tonic)
        self.i_s_screen.interval_note_playback_requested.subscribe(self.play_i_s_interval_note)
        self.i_s_screen.multiple_choice.answer_submited.subscribe(self.process_mc_answer)
        self.i_s_screen.explanation_requested.subscribe(self.show_explanation)
        self.i_s_screen.menu_requested.subscribe(self.abandon_and_show_menu)
        self.explain_screen.next_exercise_requested.subscribe(self.next_exercise)
        self.explain_screen.menu_requested.subscribe(self.abandon_and_show_menu)
        self.eval_screen.eval_continue_pressed.subscribe(self.show_menu)
        self.p_screen.prog_playback_requested.subscribe(self.play_p_rogression)
        self.p_screen.multiple_choice.answer_submited.subscribe(self.process_mc_answer)
        self.p_screen.explanation_requested.subscribe(self.show_explanation)
        self.p_screen.menu_requested.subscribe(self.abandon_and_show_menu)
        self.c_screen.chord_playback_requested.subscribe(self.play_c_chord)
        self.c_screen.multiple_choice.answer_submited.subscribe(self.process_mc_answer)
        self.c_screen.explanation_requested.subscribe(self.show_explanation)
        self.c_screen.menu_requested.subscribe(self.abandon_and_show_menu)
        self.r_screen.rythm_plyback_requested.subscribe(self.play_r_rythm)
        self.r_screen.answer_button_pressed.subscribe(self.process_r_input)
        self.r_screen.explanation_requested.subscribe(self.show_explanation)
        self.r_screen.menu_requested.subscribe(self.abandon_and_show_menu)


    def show_menu(self): #Mostra menu de seleção de exercícios
        self.window.show_menu()

    def abandon_and_show_menu(self):
        session=self.exercise_manager.exercise_session
        if session is not None and session.mode=="midi":
            self.midi_listener.midi_key_pressed.unsubscribe(self.on_midi_input)
            self.midi_listener.stop_listening()
        self.show_menu()

    def start_exercises(self, selected_exercise, selected_difficulty, selected_exercise_num, selected_mode):
        self.exercise_manager.create_exercise_session(selected_exercise, selected_difficulty, selected_exercise_num, selected_mode) #Criar sessão com as configurações selecionadas na interface
        self.show_exercise() #Exibir exercício na interface
        if selected_mode == "midi":
            self.midi_listener.listen_for_key()
            self.midi_listener.midi_key_pressed.subscribe(self.on_midi_input)

    def show_exercise(self):
        session=self.exercise_manager.exercise_session
        state=session.view_state()
        self.window.show_exercise(session.exercise_type, session.mode, state)

    def next_exercise(self):
        session = self.exercise_manager.exercise_session
        exercise_type=session.exercise_type #Avançar para o próximo exercício
        if not session.is_finished():
            session.next_exercise()
            self.show_exercise() #Se a sessão não terminou, apresentar o próximo exercício
        else:
            self.on_session_end() #Caso contrário, apresentar avaliação do desempenho

    def show_explanation(self):
        session = self.exercise_manager.exercise_session
        explanation=session.exercise_explanation()
        self.window.show_explanation_page(explanation)

    def process_mc_answer(self, answer): #valida resposta de escolha multipla e mostra feedback
        session = self.exercise_manager.exercise_session
        session.validate_answer(answer)
        if session.answer_is_correct(answer):
            self.window.set_feedback("Certo!")
        else:
            self.window.set_feedback("Errado!")
        self.window.set_continue_enabled(True)
        self.window.show_feedback()

    def process_r_input(self):
        current_time=time.perf_counter()
        session=self.exercise_manager.exercise_session
        session.play_input_sound()
        session.validate_input(current_time)
        if session.exercise_answered:
            feedback=session.get_last_rating_feedback()
            self.window.set_feedback(feedback)
            self.window.show_feedback()
            self.window.set_continue_enabled(True)

    def on_midi_input(self, midi_key):
        session = self.exercise_manager.exercise_session
        session.receive_input(midi_key)
        self.window.set_feedback(session.last_feedback)
        self.window.show_feedback()
        self.window.set_midi_feedback(session.get_input_feedback())
        if session.exercise_answered:
            self.window.set_continue_enabled(True)

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
            self.midi_listener.midi_key_pressed.unsubscribe(self.on_midi_input)
            self.midi_listener.stop_listening()
        self.show_eval()

    def show_eval(self):
        session = self.exercise_manager.exercise_session
        session.set_result_stats()
        results=session.get_result_stats()
        self.window.show_evaluation_page(results)

main=Main()
sys.exit(main.app.exec())


