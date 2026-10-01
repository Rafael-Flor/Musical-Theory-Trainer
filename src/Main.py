from PySide6 import QtWidgets


from src.ExerciseManager.exercise_manager import ExerciseManager
from src.Gui.gui import MainWindow
import sys


class Main:
    def __init__(self):

        self.exercise_manager = ExerciseManager() #Gestor de exercícios

        #Inicializar interface gráfica
        self.app = QtWidgets.QApplication([])
        self.window = MainWindow()
        self.window.resize(800, 600)
        self.window.show()

        #Ecrãs da interface
        self.config_screen = self.window.config_page
        self.i_s_screen = self.window.int_scale_exercise_page
        self.explain_screen = self.window.explanation_page
        self.eval_screen = self.window.evaluation_page

        #Conectar os eventos da interface às ações a tomar
        self.config_screen.exercise_configured.subscribe(self.start_exercises)
        self.i_s_screen.tonic_playback_requested.subscribe(self.play_i_s_tonic)
        self.i_s_screen.interval_note_playback_requested.subscribe(self.play_i_s_interval_note)
        self.i_s_screen.answer_submited.subscribe(self.process_i_s_answer)
        self.i_s_screen.explanation_requested.subscribe(self.show_explanation)
        self.explain_screen.next_exercise_requested.subscribe(self.next_exercise)
        self.eval_screen.eval_continue_pressed.subscribe(self.show_menu)

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
            self.show_eval() #Caso contrário, apresentar avaliação do desempenho

    def show_exercise(self, selected_exercise): #Mostra o exercício na interface
        match selected_exercise:
            case "interval_scale":
                self.show_i_s_exercise()

    def show_i_s_exercise(self): #Mostra um exercício de reconhecimento de intervalos em escalas na interface
        session = self.exercise_manager.exercise_session
        scale_info = session.current_exercise_scale_info()
        options = session.exercise_answer_options()
        self.window.show_interval_scale_page(scale_info, options)

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


    def play_i_s_tonic(self):
        session = self.exercise_manager.exercise_session
        session.play_exercise_tonic()
    def play_i_s_interval_note(self):
        session = self.exercise_manager.exercise_session
        session.play_exercise_interval_note()

    def show_eval(self):
        session = self.exercise_manager.exercise_session
        session.set_result_stats()
        self.window.show_evaluation_page(session.correct_count, session.accuracy, session.evaluation)



main=Main()
sys.exit(main.app.exec())


