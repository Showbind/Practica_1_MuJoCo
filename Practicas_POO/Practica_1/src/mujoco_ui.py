import customtkinter
import threading
import sys
from src.mujoco_simulador import OpenMujoco




class Tkinter_UI(object):
    def __init__(self, xml_path):
        # Modo Interfaz
        customtkinter.set_appearance_mode("dark")

        # Hilo MuJoCo
        self.thread_is_running = False # Estado
        self.mujoco_thread = threading.Thread(target=self.run_mujoco, daemon= True) # Definir hilo

        # Path del objeto de MuJoCo
        self.xml_path = xml_path

        # Inicialización del objeto
        self.mujoco_executable = None

        # Main Window
        self.app = customtkinter.CTk()
        self.app.title("MuJoCo: UI_Panel")
        self.app.geometry("960x540")
    
        # WIDGETS

        # Definir nº filas & columnas
        self.app.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), weight=1)
        self.app.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), weight=1)

        # Fonts
        self.font_helvetica_14 = customtkinter.CTkFont(family="helvetica", size=14)
        self.font_arial_30 = customtkinter.CTkFont(family="arial", size=30)

        # FRAME_IZQUIERDO

        # Propiedades
        self.frame_left = customtkinter.CTkFrame(master=self.app, width=150, height=600,border_color="#560d15")
        self.frame_left.grid(row=0, column=0,rowspan=15,columnspan = 1, padx=2, pady=2, sticky="nsew")
        self.frame_left.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), weight=1)
        self.frame_left.grid_propagate(False)

        # Etiqueta_0
        self.label = customtkinter.CTkLabel(self.frame_left, text="MuJoCo", font=self.font_arial_30, fg_color="#2b2b2b")
        self.label.grid(row=0, column=0, padx=33, pady=20, sticky="w")

        # Menu Desplegable
        self.menu_spheres = customtkinter.CTkOptionMenu(self.frame_left, values=["Esfera Roja", "Esfera Azul"], command=self.menu_event_sphere) 
        self.menu_spheres.set("Red Sphere")
        self.menu_spheres.grid(row=12, column=0, padx=19, pady=0, sticky="w")

        # Boton Ejecutar MuJoCo
        self.button_run_app = customtkinter.CTkButton(self.frame_left, command=self.button_event_run_mujoco, text= "Ejecutar MuJoCo")
        self.button_run_app.grid(row=1, column=0, padx=19, pady=8, sticky="w")

        # APP_FRAME       
        
        # Slider
        self.slider_object_size = customtkinter.CTkSlider(master=self.app, from_=0.01, to=0.3, command=self.slider_event_resize_object)
        self.slider_object_size.grid(row=12, column=5, padx=0, pady=0, sticky="w")
        
        # Etiqueta_1
        self.label_1 = customtkinter.CTkLabel(self.app, text="Sphere size", fg_color="transparent")
        self.label_1.grid(row=12, column=4, padx=0, pady=0, sticky="w")

    # CALLBACKS

    # Ejecuta MuJoCo
    def button_event_run_mujoco(self): 
        if self.thread_is_running == False: 
            self.thread_is_running = True 
            self.mujoco_thread.start()

        elif self.mujoco_thread.is_alive() == False and self.thread_is_running == True:
            print("Cierre esta ventana para volver a ejecutar el simulador")
        else:
            print("Ya hay iniciada una instancia de MuJoCo")

    # Cambia el tamaño de la esfera
    def slider_event_resize_object(self, value): 
        print(f"    -Tamaño Esfera: {value}")
        self.mujoco_executable.update_object_properties(new_size=value,new_object_name=self.mujoco_executable.object_name)

    # Pasa el nombre de la esfera 
    def menu_event_sphere(self, value): 
        match value:
            case "Esfera Roja":
                value = "red_sphere"
            case "Esfera Azul":
                value = "blue_sphere"
            case _:
                sys.exit("Los nombres de los valores del menu desplegable 'Esferas', o los del xml han sido cambiados. Necesitan ser actualizados")

        self.mujoco_executable.update_object_properties(new_size=None, new_object_name=value) # Envia el nuevo nombre

    #EJECUTAR PROGRAMA

    # Ejecuta CustomTkinter
    def start(self):
        self.app.mainloop()

    # Ejecuta MuJoCo
    def run_mujoco(self): 
        self.mujoco_executable = OpenMujoco(960,540,self.xml_path)
        self.mujoco_executable.run()

def main():
    programa = Tkinter_UI("Practicas_POO\\Practica_1\\src\\models\\esfera.xml")
    programa.start()

if __name__ == "__main__":
    main()