import customtkinter
import threading
from mujoco_simulador import openMujoco

class programa(object):
    def __init__(self, xml_path):
    #-----------------------------------------------------------
    #                       INICIALIZACIÓN
    #-----------------------------------------------------------
        # Modo Interfaz
        customtkinter.set_appearance_mode("dark")

        # Estado del hilo
        self.thread_is_running = False

        # Path del objeto de MuJoCo
        self.xml_path = xml_path

        # Inicialización del objeto
        self.mujoco_executable = None

        # Main Window
        self.app = customtkinter.CTk()
        self.app.title("tinker")
        self.app.geometry("960x540")

        # configure grid layout (4x4)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_columnconfigure((2, 3), weight=0)
        self.app.grid_rowconfigure((0, 1, 2), weight=1)

    #-----------------------------------------------------------
    #                       WIDGETS
    #-----------------------------------------------------------
        self.slider_object_size = customtkinter.CTkSlider(master=self.app, from_=0.1, to=2, command=self.slider_event_resize_object)
        self.slider_object_size.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        self.button_run_app = customtkinter.CTkButton(master=self.app, command=self.button_run_mujoco)
        self.button_run_app.grid(row=10, column=3, padx=10, pady=5, sticky="w")

    def run(self):
        self.app.mainloop()
        
#-----------------------------------------------------------
#                       WIDGETS
#-----------------------------------------------------------
    def slider_event_resize_object(self, value): # Cambia el tamaño de la esfera
        self.size = value
        self.mujoco_executable.update_object_size(self.size)

    def run_mujoco(self): # Ejecuta la simulacion
        self.mujoco_executable
        self.mujoco_executable = openMujoco(960,540,self.xml_path)
    # mujoco_executable.size = size
        self.mujoco_executable.run()

    def button_run_mujoco(self): # Ejecuta MuJoCo
        self.thread_is_running
        if self.thread_is_running == False: # Ejecuta MuJoCo
            self.thread_is_running = True
            threading.Thread(target=self.run_mujoco, daemon= True).start()
        else:
            print("Ya hay iniciada una instancia de MuJoCo")

def main():
    p = programa("Practicas_POO\\Practica_1\\src\\models\\esfera.xml")
    p.run()

if __name__ == "__main__":
    main()