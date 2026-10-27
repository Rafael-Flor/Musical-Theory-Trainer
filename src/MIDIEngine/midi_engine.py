import time

import mido

from src.Events import Event


class MidiListener:

    def __init__(self):
        self.midi_key_pressed = Event()
        self.port=None


    def listen_for_key(self):
        if self.port is not None:
            return
        try:
            self.port=mido.open_input(callback=self._on_message)
        except OSError as e:
            raise  OSError(f"Não foi possível abrir o dispositivo MIDI: {e}") from e

    def _on_message(self, message):
        if message.type == "note_on" and message.velocity > 0:
            self.midi_key_pressed.emit(message.note)

    def stop_listening(self):
        if self.port is None:
            return
        port=self.port
        self.port = None
        port.close()
        print("Port closed")
