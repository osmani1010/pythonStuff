from pygame import mixer

class SoundManager:
    def __init__(self):
        mixer.init()
        self.sounds = {
            'place': mixer.Sound('assets/place.wav'),
            'invalid': mixer.Sound('assets/invalid.wav'),
            'win': mixer.Sound('assets/win.wav')
        }
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()