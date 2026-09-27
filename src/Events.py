class Event: #Define um evento
    def __init__(self):
        self.listeners = [] #Lista de métodos interessados no evento

    def subscribe(self, listener): #Registar o interesse de um método no evento
        self.listeners.append(listener)

    def emit(self, *args, **kwargs): #Quando o evento ocorre, chamar todos os métodos interessados com os argumentos recebidos
        for listener in self.listeners:
            listener(*args, **kwargs)
            