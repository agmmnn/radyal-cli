from abc import ABC, abstractmethod


class DictBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def show(self):
        pass
