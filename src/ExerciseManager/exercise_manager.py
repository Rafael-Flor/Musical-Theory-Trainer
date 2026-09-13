from src.ExerciseGenerator.exercise_generator import ExerciseGenerator
from src.MusicTheoryModel.music_theory_model import MusicTheoryModel

class ExerciseSession:
    def __init__(self, exercises, audio_engine):
        self.audio_engine=audio_engine
        self.exercises=exercises
        self.current_exercise=0

class IntervalScaleSession(ExerciseSession):
    def __init__(self,exercises, audio_engine):
        super().__init__(exercises, audio_engine)


class ExerciseManager:

    def __init__(self):
        self.theory_model=MusicTheoryModel()
        self.exercise_generator=ExerciseGenerator(self.theory_model)
        self.audio_engine=None
        self.exercise_session=None


    def create_exercise_session(self, selected_exercise,selected_difficulty, selected_exercise_num, selected_mode):
        generator=self.exercise_generator
        exercises=[]
        if selected_mode == "gui": generate_options=True
        else: generate_options=False
        match selected_exercise:
            case "interval_scale":
                for i in range(selected_exercise_num):
                    exercises.append(generator.generate_scale_interval_exercise(selected_difficulty,generate_options))
                self.exercise_session=IntervalScaleSession(exercises,self.audio_engine)


