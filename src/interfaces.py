from abc import ABC, abstractmethod

class Runtime_Interface(ABC):
    @abstractmethod
    def run(self):
        pass

class Canvas(ABC):
    @abstractmethod
    def draw_axis(self):
        pass

    @abstractmethod
    def draw_graph(self):
        pass

class Read_Json(ABC):
    @abstractmethod
    def open_json_file(self):
        pass

    def read_file(self):
        pass