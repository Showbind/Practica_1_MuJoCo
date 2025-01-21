from abc import ABC, abstractmethod
from datetime import datetime

class RuntimeInterface(ABC):
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

class ReadJson(ABC):
    @abstractmethod
    def open_json_file(self):
        pass

    def read_file(self):
        pass

class DataOutOfGraphError(Exception):
    def __init__(self, sphere: str):
        error_message = f"La posición del eje x de la esfera {sphere} está fuera de los límites de la gráfica."
        super().__init__(f"Error:  {error_message} ")

class DataLog:
    def __init__(self, type: str):
            actual_date =  datetime.now().strftime("%d-%m_%H-%M-%S")
            self.logfile_path = f"logs\\log_{type}_{actual_date}"
            self.log_file = open(self.logfile_path, "w")

    def write_log_file(self, message_type: str, message: str):
        time = datetime.now().strftime("%H:%M:%S")
        self.log_file.write(f"[{time}] [{message_type}]: {message} \n")