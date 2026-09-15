import threading
import tinysoundfont
import  time


class AudioEngine:
    def __init__(self):
        self.synth = tinysoundfont.Synth()
        self.soundfont = self.synth.sfload("../AudioEngine/YDP-GrandPiano.sf2")
        self.synth.program_select(0, self.soundfont, 0, 0)
        self.play_thread=None
        self.synth.start()




    def is_playing(self): #Verifica se existe uma thread de reprodução ativa
        if self.play_thread is not None and self.play_thread.is_alive():
            return True
        else: return False

    def play_note(self,note, duration, octave_shift=0): #Inicia um thread para reprodução de uma nota
        if self.is_playing(): return #Apenas um thread de reprodução ativo a cada instante
        self.play_thread = threading.Thread(target=self._play_note, args=(note, duration, octave_shift),daemon=True)
        self.play_thread.start()

    def _play_note(self, note, duration, octave_shift=0): #Reproduz uma nota
        self.synth.noteon(0, note.pitch + 12 * octave_shift, 100)
        time.sleep(duration) #Controla a duração da nota
        self.synth.noteoff(0, note.pitch + 12 * octave_shift)
        time.sleep(0.5) #Controla a duração da libertação da nota

    def play_note_sequence(self, sequence, note_duration, octave_shift=0): #Inicia um thread para reprodução de notas em sequência
        if self.is_playing(): return
        self.play_thread = threading.Thread(target=self._play_note_sequence, args=(sequence, note_duration, octave_shift),daemon=True)
        self.play_thread.start()

    def _play_note_sequence(self, sequence, note_duration, octave_shift=0): #Reproduz uma sequência de notas
        for note in sequence:
            self.synth.noteon(0, note.pitch + 12 * octave_shift, 100)
            time.sleep(note_duration)
            self.synth.noteoff(0, note.pitch + 12 * octave_shift)
            time.sleep(0.5)


