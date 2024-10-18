import customtkinter
import threading
from mujoco_simulador import OpenMujoco

class Tkinter_UI(object):
    def __init__(self, xml_path):
        # Modo Interfaz
        customtkinter.set_appearance_mode("dark")

        # Thread
        self.thread_is_running = False # Estado
        self.mujoco_thread = threading.Thread(target=self.run_mujoco, daemon= True) # Definir hilo

        # Path del objeto de MuJoCo
        self.xml_path = xml_path

        # Inicialización del objeto
        self.mujoco_executable = None

        # Main Window
        self.app = customtkinter.CTk()
        self.app.title("tinker")
        self.app.geometry("960x540")

        #configure grid layout (4x4)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_columnconfigure((2, 3), weight=0)
        self.app.grid_rowconfigure((0, 1, 2), weight=1)

    #-----------------------------------------------------------
    #                       WIDGETS
    #-----------------------------------------------------------
        self.slider_object_size = customtkinter.CTkSlider(master=self.app, from_=0.1, to=2, command=self.slider_event_resize_object)
        self.slider_object_size.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        self.button_run_app = customtkinter.CTkButton(master=self.app, command=self.button_event_run_mujoco)
        self.button_run_app.grid(row=10, column=3, padx=10, pady=5, sticky="w")

#-----------------------------------------------------------
#                       CALLBACKS
#-----------------------------------------------------------
    def button_event_run_mujoco(self): # Ejecuta MuJoCo

        if self.thread_is_running == False: # Ejecuta MuJoCo
            self.thread_is_running = True 
            self.mujoco_thread.start()

        elif self.mujoco_thread.is_alive() == False and self.thread_is_running == True:
            print("Cierre esta ventana para volver a ejecutar el simulador")
        else:
            print("Ya hay iniciada una instancia de MuJoCo")
            
    def slider_event_resize_object(self, value): # Cambia el tamaño de la esfera
        self.size = value
        self.mujoco_executable.update_object_properties(self.size)

#-----------------------------------------------------------
#                     EJECUTAR PROGRAMA
#-----------------------------------------------------------
    def run_mujoco(self): # Ejecuta la simulacion
        self.mujoco_executable = OpenMujoco(960,540,self.xml_path)
        self.mujoco_executable.run()
        
    def start(self):
        self.app.mainloop()
        

def main():
    programa = Tkinter_UI("Practicas_POO\\Practica_1\\src\\models\\esfera.xml")
    programa.start()

if __name__ == "__main__":
    main()