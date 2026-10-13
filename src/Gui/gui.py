
from PySide6 import QtCore, QtWidgets

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
        self.explanation_page = ExplanationPage()
        self.evaluation_page = EvaluationPage()

        #Adicionar páginas às páginas da interface
        self.pages.addWidget(self.main_menu)
        self.pages.addWidget(self.config_page)
        self.pages.addWidget(self.int_scale_exercise_page)
        self.pages.addWidget(self.prog_exercise_page)
        self.pages.addWidget(self.explanation_page)
        self.pages.addWidget(self.evaluation_page)

        #Tornar a estrutura de páginas o objeto central da interface
        self.setCentralWidget(self.pages)

        #Conectar os sinais emitidos às ações a tomar
        self.main_menu.exercise_selected.connect(self.show_config_page)


    def show_config_page(self,exercise_title, exercise_code): #Mostra a página de configuração
        self.config_page.set_exercise(exercise_title, exercise_code) #Atualizar página com informação do exercício
        self.pages.setCurrentWidget(self.config_page) #Mostrar a página de configuração

    def show_menu(self):
        self.pages.setCurrentWidget(self.main_menu)

    def show_interval_scale_page(self, scale_info, options):
        self.int_scale_exercise_page.set_current_exercise(scale_info)
        self.int_scale_exercise_page.set_answer_options(options)
        self.int_scale_exercise_page.enable_options()
        self.pages.setCurrentWidget(self.int_scale_exercise_page)

    def show_prog_page(self, prog_info, options):
        self.prog_exercise_page.set_current_exercise(prog_info)
        self.prog_exercise_page.set_answer_options(options)
        self.prog_exercise_page.enable_options()
        self.pages.setCurrentWidget(self.prog_exercise_page)

    def show_explanation_page(self, explanation):
        self.explanation_page.set_explanation(explanation)
        self.pages.setCurrentWidget(self.explanation_page)

    def show_evaluation_page(self, correct_count, accuracy, evaluation):
        self.evaluation_page.set_stats(correct_count, accuracy, evaluation)
        self.pages.setCurrentWidget(self.evaluation_page)

class MainMenu(QtWidgets.QWidget): #Página do menu principal
    exercise_selected = QtCore.Signal(str, str) #Sinal a emitir quando um exercício for selecionado
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

        #Criar elementos da página
        self.interval_scale_title = "Exercícios de reconhecimento de intervalos em escalas"
        self.interval_scale_code = "interval_scale"
        self.prog_title = "Exercícios de reconhecimento de progressões harmónicas"
        self.prog_code = "harmonic_prog"
        self.interval_scale_bt=QtWidgets.QPushButton(self.interval_scale_title)
        self.interval_scale_bt.clicked.connect(lambda: self.exercise_selected.emit(self.interval_scale_title,self.interval_scale_code)) #Quando clicar no botão emitir o sinal de seleção de exercício
        self.prog_bt = QtWidgets.QPushButton(self.prog_title)
        self.prog_bt.clicked.connect(lambda: self.exercise_selected.emit(self.prog_title,self.prog_code))

        #Adicionar elementos ao layout da página
        self.layout.addWidget(self.interval_scale_bt)
        self.layout.addWidget(self.prog_bt)



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


    def set_exercise(self, exercise_title, exercise_code): #Atualiza a página com a informação do exercício escolhido
        self.selected_exercise = exercise_code
        self.title.setText(exercise_title)

    def confirm_config(self): #Emite um evento com as configurações selecionadas
        selected_exercise = self.selected_exercise
        selected_difficulty = self.set_difficulty.currentData()
        selected_exercise_num = self.set_exercise_num.currentData()
        selected_mode = self.set_mode.currentData()
        self.exercise_configured.emit(selected_exercise,selected_difficulty,selected_exercise_num,selected_mode)


class ExPage(QtWidgets.QWidget): #Página para resolução de exercícios
    #Criar eventos
    explanation_requested = Event() #Pedir explicação do exercício
    answer_submited = Event() #Resposta foi submetida

    def __init__(self):
        super().__init__()

        self.options=None

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 50, 0, 0)

        self.title=QtWidgets.QLabel("")
        self.instructions=QtWidgets.QLabel("")

        self.multiple_choice_txt = QtWidgets.QLabel("")

        self.feedback=QtWidgets.QLabel("")

        self.op1_bt = QtWidgets.QPushButton("")
        self.op1_bt.clicked.connect(lambda: self.op_bt_clicked(self.options[0]))
        self.op2_bt = QtWidgets.QPushButton("")
        self.op2_bt.clicked.connect(lambda: self.op_bt_clicked(self.options[1]))
        self.op3_bt = QtWidgets.QPushButton("")
        self.op3_bt.clicked.connect(lambda: self.op_bt_clicked(self.options[2]))
        self.op4_bt = QtWidgets.QPushButton("")
        self.op4_bt.clicked.connect(lambda: self.op_bt_clicked(self.options[3]))

        self.continue_bt=QtWidgets.QPushButton("Continuar")
        self.continue_bt.clicked.connect(lambda: self.explanation_requested.emit())

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.instructions)
        self.layout.addWidget(self.multiple_choice_txt)

        self.layout.addWidget(self.op1_bt)
        self.layout.addWidget(self.op2_bt)
        self.layout.addWidget(self.op3_bt)
        self.layout.addWidget(self.op4_bt)

        self.layout.addWidget(self.feedback)
        self.layout.addWidget(self.continue_bt)

    def set_answer_options(self, options): #Atualiza botões das opções de resposta
        self.options=options
        self.op1_bt.setText(str(options[0]))
        self.op2_bt.setText(str(options[1]))
        self.op3_bt.setText(str(options[2]))
        self.op4_bt.setText(str(options[3]))

    def set_feedback(self, feedback): #Atualiza o feedback da resposta
        self.feedback.setText(feedback)
    def show_feedback(self): #Mostra o feedback da resposta
        self.feedback.show()

    def enable_options(self): #Ativa opções de resposta
        self.op1_bt.setDisabled(False)
        self.op2_bt.setDisabled(False)
        self.op3_bt.setDisabled(False)
        self.op4_bt.setDisabled(False)

    def op_bt_clicked(self, option): #Emite opção escolhida e desativa os botões de resposta
        self.answer_submited.emit(option)
        self.op1_bt.setDisabled(True)
        self.op2_bt.setDisabled(True)
        self.op3_bt.setDisabled(True)
        self.op4_bt.setDisabled(True)

class IntervalScaleExPage(ExPage): #Página para resolução de exercícios de reconhecimento de intervalos em escalas

    tonic_playback_requested = Event()  # Pedir reprodução da tónica
    interval_note_playback_requested = Event()  # Pedir reprodução da nota do intervalo

    def __init__(self):
        super().__init__()
        self.title.setText("Exercício de reconhecimento de intervalos em escalas")
        self.instructions.setText("Clique nos botões abaixo para reproduzir as notas do exercício")
        self.multiple_choice_txt.setText("Selecione o grau da nota do intervalo:")
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

class ExplanationPage(QtWidgets.QWidget):
    next_exercise_requested = Event()
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 50, 0, 0)

        self.explanation=QtWidgets.QLabel("")
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

        self.correct_stat=QtWidgets.QLabel("")
        self.precision_stat = QtWidgets.QLabel("")
        self.eval_stat = QtWidgets.QLabel("")

        self.continue_bt = QtWidgets.QPushButton("Continuar")
        self.continue_bt.clicked.connect(lambda: self.eval_continue_pressed.emit())

        self.layout.addWidget(self.correct_stat)
        self.layout.addWidget(self.precision_stat)
        self.layout.addWidget(self.eval_stat)
        self.layout.addWidget(self.continue_bt)

    def set_stats(self, correct_count, accuracy, evaluation): #Atualiza as estatiscas de avaliação
        self.correct_stat.setText("Respostas corretas: "+str(correct_count))
        self.precision_stat.setText("Precisão: "+str(accuracy))
        self.eval_stat.setText("Avaliação: " + str(evaluation))








