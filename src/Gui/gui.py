
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QHBoxLayout, QFrame

from src.Events import Event



class MainWindow(QtWidgets.QMainWindow): #Janela da interface gráfica
    def __init__(self):
        super().__init__()

        self.pages = QtWidgets.QStackedWidget() #Guarda Páginas(Ecrãs) da interface

        #Instanciar páginas da interface
        self.main_menu = MainMenu()
        self.config_page = ConfigPage()
        self.int_scale_exercise_page = IntervalScaleExPage()
        self.prog_exercise_page= ProgExPage()
        self.chord_exercise_page=ChordExPage()
        self.rythm_exercise_page= RythmExPage()
        self.explanation_page = ExplanationPage()
        self.evaluation_page = EvaluationPage()

        #Adicionar páginas às páginas da interface
        self.pages.addWidget(self.main_menu)
        self.pages.addWidget(self.config_page)
        self.pages.addWidget(self.int_scale_exercise_page)
        self.pages.addWidget(self.prog_exercise_page)
        self.pages.addWidget(self.chord_exercise_page)
        self.pages.addWidget(self.rythm_exercise_page)
        self.pages.addWidget(self.explanation_page)
        self.pages.addWidget(self.evaluation_page)

        #Tornar a estrutura de páginas o objeto central da interface
        self.setCentralWidget(self.pages)

        #Conectar os sinais emitidos às ações a tomar
        self.main_menu.exercise_selected.connect(self.show_config_page)


    def show_config_page(self,exercise_title, exercise_code, modes): #Mostra a página de configuração
        self.config_page.set_exercise(exercise_title, exercise_code, modes) #Atualizar página com informação do exercício
        self.pages.setCurrentWidget(self.config_page) #Mostrar a página de configuração

    def show_menu(self):
        self.pages.setCurrentWidget(self.main_menu)

    def show_mc_interval_scale_page(self, scale_info, options):
        self.int_scale_exercise_page.set_current_exercise(scale_info)
        if self.int_scale_exercise_page.current_mode != "mc":
            self.int_scale_exercise_page.enable_multiple_choice()
        self.int_scale_exercise_page.multiple_choice.set_answer_options(options)
        self.int_scale_exercise_page.multiple_choice.enable_options()
        self.pages.setCurrentWidget(self.int_scale_exercise_page)

    def show_midi_interval_scale_page(self, scale_info, input_len):
        self.int_scale_exercise_page.set_current_exercise(scale_info)
        if self.int_scale_exercise_page.current_mode != "midi":
            self.int_scale_exercise_page.enable_midi()
        self.int_scale_exercise_page.midi_feedback.set_feedback_widget(input_len)
        self.pages.setCurrentWidget(self.int_scale_exercise_page)

    def show_prog_page(self, prog_info, options):
        self.prog_exercise_page.set_current_exercise(prog_info)
        self.prog_exercise_page.multiple_choice.set_answer_options(options)
        self.prog_exercise_page.multiple_choice.enable_options()
        self.pages.setCurrentWidget(self.prog_exercise_page)

    def show_mc_chord_page(self, chord_info, options):
        if self.chord_exercise_page.current_mode != "mc":
            self.chord_exercise_page.enable_multiple_choice()
        self.chord_exercise_page.set_current_exercise(chord_info)
        self.chord_exercise_page.multiple_choice.set_answer_options(options)
        self.chord_exercise_page.multiple_choice.enable_options()
        self.pages.setCurrentWidget(self.chord_exercise_page)

    def show_midi_chord_page(self, chord_info, input_len):
        if self.chord_exercise_page.current_mode != "midi":
            self.chord_exercise_page.enable_midi()
        self.chord_exercise_page.set_current_exercise(chord_info)
        self.chord_exercise_page.midi_feedback.set_feedback_widget(input_len)
        self.pages.setCurrentWidget(self.chord_exercise_page)

    def show_exercise(self, exercise_id, mode, state): #Mostra o exercício na interface
        match exercise_id, mode:
            case "interval_scale", "gui":
                self.show_mc_interval_scale_page(state.info, state.options)
            case "interval_scale", "midi":
                self.show_midi_interval_scale_page(state.info, state.expected_input_len)
            case "harmonic_prog", "gui":
                self.show_prog_page(state.info, state.options)
            case "chord", "gui":
                self.show_mc_chord_page(state.info, state.options)
            case "chord", "midi":
                self.show_midi_chord_page(state.info, state.expected_input_len)
            case "rythm":
                self.show_rythm_page()

    def show_rythm_page(self):
        self.pages.setCurrentWidget(self.rythm_exercise_page)

    def set_feedback(self, txt):
        current_page=self.pages.currentWidget()
        if isinstance(current_page, ExPage) or isinstance(current_page, RythmExPage):
            current_page.set_feedback(txt)

    def show_feedback(self):
        current_page = self.pages.currentWidget()
        if isinstance(current_page, ExPage) or isinstance(current_page, RythmExPage):
            current_page.show_feedback()

    def set_midi_feedback(self,flags):
        current_page = self.pages.currentWidget()
        if isinstance(current_page, ExPage) or isinstance(current_page, RythmExPage):
            current_page.MIDI_feedback.set_feedback(flags)

    def show_explanation_page(self, explanation):
        self.explanation_page.set_explanation(explanation)
        self.pages.setCurrentWidget(self.explanation_page)

    def show_evaluation_page(self, results):
        self.evaluation_page.set_stats(results)
        self.pages.setCurrentWidget(self.evaluation_page)

class MainMenu(QtWidgets.QWidget): #Página do menu principal
    exercise_selected = QtCore.Signal(str, str, tuple) #Sinal a emitir quando um exercício for selecionado
    def __init__(self):
        super().__init__()

        #Configurar o layout da página
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 50, 0, 0)

        #Configurar o estilo dos elementos da página
        self.setStyleSheet(
        """
        QPushButton { text-align: left; padding: 10px; font-size: 20px }
        """)

    def set_main_menu(self, exercises):
        #Criar elementos da página
        for exercise in exercises:
            button = QtWidgets.QPushButton(exercise["title"])
            button.clicked.connect(lambda checked=False, ex=exercise: self.exercise_selected.emit(ex["title"], ex["id"], ex["modes"]))
            self.layout.addWidget(button)




class ConfigPage(QtWidgets.QWidget): #Página de configuração de exercícios

    def __init__(self):
        super().__init__()

        # Eventos a emitir ao exterior
        self.exercise_configured = Event()

        self.selected_exercise=None # Id do exercício selecionado

        self.title = QtWidgets.QLabel("") #Título da página

        #Configurar o layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 50, 0, 0)

        #Criar elementos da página
        self.set_difficulty=QtWidgets.QComboBox()
        self.set_difficulty.addItem("Fácil","easy")
        self.set_difficulty.addItem("Médio","medium")
        self.set_difficulty.addItem("Difícil","hard")

        self.set_exercise_num = QtWidgets.QComboBox()
        self.set_exercise_num.addItem("5",5)
        self.set_exercise_num.addItem("10",10)
        self.set_exercise_num.addItem("15",15)

        self.set_mode = QtWidgets.QComboBox()
        self.set_mode.addItem("Interface","gui")
        self.set_mode.addItem("Dispositivo MIDI","midi")

        self.continuar = QtWidgets.QPushButton("Continuar")

        #Adicionar elementos ao layout da página
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.set_difficulty)
        self.layout.addWidget(self.set_exercise_num)
        self.layout.addWidget(self.set_mode)
        self.layout.addWidget(self.continuar)

        self.continuar.clicked.connect(self.confirm_config)


    def set_exercise(self, exercise_title, exercise_code, modes): #Atualiza a página com a informação do exercício escolhido
        self.selected_exercise = exercise_code
        self.title.setText(exercise_title)
        self.set_mode.setCurrentIndex(0)
        model = self.set_mode.model()
        for i in range(self.set_mode.count()):
            mode_id=self.set_mode.itemData(i)
            if mode_id in modes:
                model.item(i).setEnabled(True)
            else:
                model.item(i).setEnabled(False)

    def confirm_config(self): #Emite um evento com as configurações selecionadas
        selected_exercise = self.selected_exercise
        selected_difficulty = self.set_difficulty.currentData()
        selected_exercise_num = self.set_exercise_num.currentData()
        selected_mode = self.set_mode.currentData()
        self.exercise_configured.emit(selected_exercise,selected_difficulty,selected_exercise_num,selected_mode)

class ExPage(QtWidgets.QWidget): #Página para resolução de exercícios
    #Criar eventos
    explanation_requested = Event() #Pedir explicação do exercício
    def __init__(self):
        super().__init__()
        self.current_mode=""

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 50, 0, 0)

        self.title=QtWidgets.QLabel("")
        self.instructions=QtWidgets.QLabel("")

        self.midi_txt = QtWidgets.QLabel("")
        self.midi_feedback=MIDI_feedback()

        self.multiple_choice_txt = QtWidgets.QLabel("")
        self.multiple_choice=MultipleChoice()

        self.feedback=QtWidgets.QLabel("")

        self.continue_bt=QtWidgets.QPushButton("Continuar")
        self.continue_bt.clicked.connect(lambda: self.explanation_requested.emit())

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.instructions)
        self.layout.addWidget(self.multiple_choice_txt)
        self.layout.addWidget(self.multiple_choice)
        self.layout.addWidget(self.midi_txt)
        self.layout.addWidget(self.midi_feedback)
        self.layout.addWidget(self.feedback)
        self.layout.addWidget(self.continue_bt)

    def set_feedback(self, feedback): #Atualiza o feedback da resposta
        self.feedback.setText(feedback)
    def show_feedback(self): #Mostra o feedback da resposta
        self.feedback.show()
    def enable_multiple_choice(self):
        self.multiple_choice_txt.show()
        self.multiple_choice.show()
        self.midi_txt.hide()
        self.midi_feedback.hide()
        self.current_mode="mc"
    def enable_midi(self):
        self.midi_txt.show()
        self.midi_feedback.show()
        self.multiple_choice_txt.hide()
        self.multiple_choice.hide()
        self.current_mode="midi"



class MultipleChoice(QtWidgets.QWidget):
    answer_submited = Event() #Resposta foi submetida
    def __init__(self):
        super().__init__()

        self.buttons = []

        self.layout = QHBoxLayout(self)

    def set_answer_options(self, options):
        for button in self.buttons:
            self.layout.removeWidget(button)
            button.deleteLater()
        self.buttons = []
        for option in options:
            button = QtWidgets.QPushButton(str(option))
            button.clicked.connect(lambda checked=False, op=option: self.op_bt_clicked(op))
            self.buttons.append(button)
            self.layout.addWidget(button)

    def enable_options(self): #Ativa opções de resposta
        for button in self.buttons:
            button.setEnabled(True)

    def op_bt_clicked(self, option): #Emite opção escolhida e desativa os botões de resposta
        self.answer_submited.emit(option)
        for button in self.buttons:
            button.setDisabled(True)

class MIDI_feedback(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.squares=[]

    def set_feedback_widget(self, input_n):
        if len(self.squares)  > input_n:
            while len(self.squares) > input_n:
                self.layout.removeWidget(self.squares[-1])
                self.squares[-1].deleteLater()
                self.squares.pop()
        elif len(self.squares) < input_n:
            while len(self.squares) < input_n:
                square = QFrame()
                square.setFixedSize(40, 40)
                square.setStyleSheet(
                    "QFrame { background-color: rgba(0,0,0,255); border: 1px solid rgba(255,255,255,1); border-radius: 4px }")
                self.layout.addWidget(square)
                self.squares.append(square)
        else:
            for square in self.squares:
                square.setStyleSheet("QFrame { background-color: rgba(0,0,0,255); border: 1px solid rgba(255,255,255,1); border-radius: 4px }")


    def set_feedback(self, correct_inputs):
        if not correct_inputs:
            for square in self.squares:
                square.setStyleSheet("background-color: black")
        else:
            for i in range(len(correct_inputs)):
                if correct_inputs[i]==True:
                    self.squares[i].setStyleSheet("background-color: green")
                else:
                    self.squares[i].setStyleSheet("background-color: black")




class IntervalScaleExPage(ExPage): #Página para resolução de exercícios de reconhecimento de intervalos em escalas

    tonic_playback_requested = Event()  # Pedir reprodução da tónica
    interval_note_playback_requested = Event()  # Pedir reprodução da nota do intervalo

    def __init__(self):
        super().__init__()
        self.title.setText("Exercício de reconhecimento de intervalos em escalas")
        self.instructions.setText("Clique nos botões abaixo para reproduzir as notas do exercício")
        self.multiple_choice_txt.setText("Selecione o grau da nota do intervalo:")
        self.midi_txt.setText("Introduza o intervalo reproduzido no dispositivo MIDI:")
        self.scale_info = QtWidgets.QLabel("")
        self.tonic_bt = QtWidgets.QPushButton("Reproduzir tónica")
        self.tonic_bt.clicked.connect(lambda: self.tonic_playback_requested.emit())
        self.interval_bt = QtWidgets.QPushButton("Reproduzir nota do intervalo")
        self.interval_bt.clicked.connect(lambda: self.interval_note_playback_requested.emit())

        self.layout.insertWidget(self.layout.indexOf(self.multiple_choice_txt),self.scale_info)
        self.layout.insertWidget(self.layout.indexOf(self.instructions)+1,self.tonic_bt)
        self.layout.insertWidget(self.layout.indexOf(self.tonic_bt)+1,self.interval_bt)

    def set_current_exercise(self, scale_info): #Atualiza informação da escala
        self.scale_info.setText(scale_info)

class ProgExPage(ExPage): #Página para resolução de exercícios de reconhecimento de progressões harmónicas

    prog_playback_requested = Event()

    def __init__(self):
        super().__init__()
        self.title.setText("Exercício de reconhecimento de progressões harmónicas:")
        self.instructions.setText("Clique nos botões abaixo para reproduzir a progressão do exercício:")
        self.multiple_choice_txt.setText("Selecione o tipo de progressão reproduzida:")
        self.prog_info = QtWidgets.QLabel("")
        self.prog_bt = QtWidgets.QPushButton("Reproduzir progressão")
        self.prog_bt.clicked.connect(lambda: self.prog_playback_requested.emit())

        self.layout.insertWidget(self.layout.indexOf(self.multiple_choice_txt),self.prog_info)
        self.layout.insertWidget(self.layout.indexOf(self.instructions)+1,self.prog_bt)

    def set_current_exercise(self, scale_info): #Atualiza informação da progressão
        self.prog_info.setText(scale_info)

class ChordExPage(ExPage): #Página para resolução de exercícios de reconhecimento de acordes

    chord_playback_requested = Event()

    def __init__(self):
        super().__init__()
        self.title.setText("Exercício de reconhecimento de acordes:")
        self.instructions.setText("Clique no botão abaixo para reproduzir o acorde do exercício:")
        self.midi_txt.setText("Introduza o acorde reproduzido no dispositivo MIDI:")
        self.multiple_choice_txt.setText("Selecione o tipo de acorde reproduzido:")
        self.chord_info = QtWidgets.QLabel("")
        self.chord_bt = QtWidgets.QPushButton("Reproduzir Acorde")
        self.chord_bt.clicked.connect(lambda: self.chord_playback_requested.emit())

        self.layout.insertWidget(self.layout.indexOf(self.multiple_choice_txt),self.chord_info)
        self.layout.insertWidget(self.layout.indexOf(self.instructions)+1,self.chord_bt)

    def set_current_exercise(self, chord_info): #Atualiza informação do acorde
        self.chord_info.setText(chord_info)

class RythmExPage(QtWidgets.QWidget):
    # Criar eventos
    explanation_requested = Event()  # Pedir explicação do exercício
    rythm_plyback_requested = Event()
    answer_button_pressed = Event()

    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 50, 0, 0)

        self.title = QtWidgets.QLabel("")
        self.instructions = QtWidgets.QLabel("")

        self.feedback = QtWidgets.QLabel("")

        self.rythm_bt=QtWidgets.QPushButton("Reproduzir Ritmo")
        self.rythm_bt.clicked.connect(lambda: self.rythm_plyback_requested.emit())

        self.continue_bt = QtWidgets.QPushButton("Continuar")
        self.continue_bt.clicked.connect(lambda: self.explanation_requested.emit())

        self.answer_bt=QtWidgets.QPushButton(".")
        self.answer_bt.clicked.connect(lambda: self.answer_button_pressed.emit())

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.instructions)
        self.layout.addWidget(self.rythm_bt)
        self.layout.addWidget(self.answer_bt)
        self.layout.addWidget(self.feedback)
        self.layout.addWidget(self.continue_bt)

    def set_feedback(self, feedback):  # Atualiza o feedback da resposta
        self.feedback.setText(feedback)

    def show_feedback(self):  # Mostra o feedback da resposta
        self.feedback.show()


class ExplanationPage(QtWidgets.QWidget):
    next_exercise_requested = Event()
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 50, 0, 0)

        self.explanation=QtWidgets.QLabel("")
        self.explanation.setFont(QtGui.QFont("Noto Sans Symbols 2", 10))
        self.continue_bt=QtWidgets.QPushButton("Continuar")
        self.continue_bt.clicked.connect(lambda : self.next_exercise_requested.emit())

        self.layout.addWidget(self.explanation)
        self.layout.addWidget(self.continue_bt)

    def set_explanation(self, explanation):
        self.explanation.setText(explanation)

class EvaluationPage(QtWidgets.QWidget): #Página para apresentação da avaliação de desempenho
    eval_continue_pressed = Event()
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 50, 0, 0)

        self.stats = QtWidgets.QLabel("")

        self.continue_bt = QtWidgets.QPushButton("Continuar")
        self.continue_bt.clicked.connect(lambda: self.eval_continue_pressed.emit())

        self.layout.addWidget(self.stats)
        self.layout.addWidget(self.continue_bt)

    def set_stats(self, results): #Atualiza as estatiscas de avaliação
        stats=""
        for title, stat in results:
            stats += f"{title}: {stat}\n"
        self.stats.setText(stats)








