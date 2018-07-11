import pygame, numpy
from abc import ABC, abstractmethod


class SoundBackend(ABC):
    @abstractmethod
    def init(self, freq):
        pass

    @abstractmethod
    def load_sound(self, filename):
        pass

    @abstractmethod
    def play_sound(self, filename):
        pass

    @abstractmethod
    def get_position(self):
        pass


class PygameBackend(SoundBackend):
    def init(self, freq):
        pygame.mixer.pre_init(freq, -16, 2, 2048)
        pygame.mixer.init()

    def load_sound(self, filename):
        sound = pygame.mixer.Sound(filename)
        return pygame.sndarray.array(sound)

    def play_sound(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def get_position(self):
        return pygame.mixer.music.get_pos()