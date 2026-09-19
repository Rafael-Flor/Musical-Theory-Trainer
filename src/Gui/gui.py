import sys

from PySide6 import QtCore, QtWidgets, QtGui


from src.ExerciseManager.exercise_manager import ExerciseManager



class MainWindow(QtWidgets.QMainWindow): #Janela da interface gráfica
    def __init__(self, exercise_manager):
        super().__init__()

        self.exercise_manager = exercise_manager #Gestor de exercícios

        self.pages = QtWidgets.QStackedWidget() #Guarda Páginas/Ecrãs da interface

        #Instanciar páginas da interface
        self.main_menu = MainMenu()
        self.config_page = ConfigPage()

        #Adicionar páginas às páginas da interface
        self.pages.addWidget(self.main_menu)
        self.pages.addWidget(self.config_page)

        #Tornar a estrutura de páginas o objeto central da interface
        self.setCentralWidget(self.pages)

        #Conectar os sinais emitidos às ações a tomar
        self.main_menu.exercise_selected.connect(self.show_config_page)

    def show_config_page(self,exercise_title, exercise_code): #Mostra a página de configuração
        self.config_page.set_exercise(exercise_title, exercise_code) #Atualizar página com informação do exercício
        self.pages.setCurrentWidget(self.config_page) #Mostrar a página de configuração

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
        self.interval_scale_bt=QtWidgets.QPushButton(self.interval_scale_title)
        self.interval_scale_bt.clicked.connect(lambda: self.exercise_selected.emit(self.interval_scale_title,self.interval_scale_code)) #Quando clicar no botão emitir o sinal de seleção de exercício

        #Adicionar elementos ao layout da página
        self.layout.addWidget(self.interval_scale_bt)



class ConfigPage(QtWidgets.QWidget): #Página de configuração de exercícios
    exercise_configured = QtCore.Signal(str, str, int, str) #Sinal a emitir quando concluir configuração do exercício
    def __init__(self):
        super().__init__()

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

    def confirm_config(self): #Emite um sinal com as configurações selecionadas
        selected_exercise = self.selected_exercise
        selected_difficulty = self.set_difficulty.currentData()
        selected_exercise_num = self.set_exercise_num.currentData()
        selected_mode = self.set_mode.currentData()
        self.exercise_configured.emit(selected_exercise,selected_difficulty,selected_exercise_num,selected_mode)
