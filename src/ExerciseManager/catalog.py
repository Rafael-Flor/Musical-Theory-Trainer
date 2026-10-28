EXERCISES=( #Definições dos exercícios disponibilizados
    {
        "id": "interval_scale",
        "title": "Exercícios de reconhecimento de intervalos em escalas",
        "modes": ("gui", "midi"),
    },
    {
        "id": "harmonic_prog",
        "title": "Exercícios de reconhecimento de progressões harmónicas",
        "modes": ("gui",)
    },
    {
        "id": "chord",
        "title": "Exercícios de reconhecimento de acordes",
        "modes": ("gui","midi")
    },
    {
        "id": "rythm",
        "title": "Exercícios de reconhecimento e execução de ritmos",
        "modes": ("gui",)
    }
)

def get_exercise(exercise_id): #retorna a informação do exercício com id correspondente
    for item in EXERCISES:
        if item["id"] == exercise_id:
            return item
    raise ValueError("Exercicio desconhecido")