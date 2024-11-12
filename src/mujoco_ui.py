from src.mujoco_simulador import OpenMujoco
from tkinter import filedialog
import json
import customtkinter
import threading
import sys

class Tkinter_UI(object):
    def __init__(self, xml_path):

        # Modo Interfaz
        customtkinter.set_appearance_mode("dark")

        # Flags
        self.file_exists = False

        # Hilo MuJoCo
        self.thread_is_running = False # Estado del hilo
        self.mujoco_thread = threading.Thread(target=self.run_mujoco, daemon= True) # Definir hilo

        # Path del archivo xml de MuJoCo
        self.xml_path = xml_path

        # Inicialización del objeto
        self.mujoco_app = None

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
        self.menu_spheres = customtkinter.CTkOptionMenu(self.frame_left, values=["Esfera Izquierda", "Esfera Derecha"], command=self.select_sphere) 
        self.menu_spheres.set("Esfera Izquierda")
        self.menu_spheres.grid(row=12, column=0, padx=19, pady=0, sticky="w")

        # Boton Ejecutar MuJoCo
        self.button_run_app = customtkinter.CTkButton(self.frame_left, command=self.button_run_mujoco, text= "Ejecutar MuJoCo")
        self.button_run_app.grid(row=1, column=0, padx=19, pady=8, sticky="w") 

        # Boton abrir ventana para elegir archivo de configuracion
        self.open_file_dialog = customtkinter.CTkButton(self.frame_left, command=self.open_json_file, text= "Abrir archivo")
        self.open_file_dialog.grid(row=2, column=0, padx=19, pady=8, sticky="w") 

    # APP_FRAME       
        
        # Slider tamaño esfera
        self.slider_resize_object = customtkinter.CTkSlider(master=self.app, from_=0.01, to=0.3, command=self.resize_object)
        self.slider_resize_object.grid(row=12, column=5, padx=0, pady=0, sticky="w")
        
        # Etiqueta_1
        self.label_1 = customtkinter.CTkLabel(self.app, text="Sphere size", fg_color="transparent")
        self.label_1.grid(row=12, column=4, padx=0, pady=0, sticky="w")

# CALLBACKS 

    # Abre el archivo de configuracion de la simulacion
    def open_json_file(self):
        self.filepath = filedialog.askopenfilename(title="Abrir archivo configuración simulador", initialdir="./src/MuJoCo_config_files", filetypes=[("Archivos JSON", "*.json"),("Archivos .txt","*.txt")])
       
        try: 
            self.file = open(file=self.filepath)
        except OSError:
            print("Error: No se ha elegido ningun archivo o el archivo ha crasheado")
        else:  # Llama a la funcion para leer el archivo
            self.file_exists = True

    # Lee e interpreta el archivo 
    def read_file(self):
        self.config_file = self.file.read()
        try:
            self.js = json.loads(self.config_file)
        except json.JSONDecodeError:
            print("\n     -Error: Formato del JSON incorrecto. Se cargará la configuración predeterminada.\n")
        else: # Carga los ajustes seleccionados
            self.mujoco_app.set_json_object_properties(self.js) 
            print("\n     - Archivo JSON valido. Se cargará la configuración.\n")

    # Ejecuta MuJoCo
    def button_run_mujoco(self): 
        if self.thread_is_running == False: 
            self.thread_is_running = True 
            self.mujoco_thread.start()
        elif self.mujoco_thread.is_alive() == False and self.thread_is_running == True:
            print("Simulacion finalizada. Cierre la UI")
        else:   
            print("Ya hay iniciada una instancia de MuJoCo")

    # Pasa el tamaño de la esfera
    def resize_object(self, value): 
        print(f"    -Tamaño Esfera: {value}")
        self.mujoco_app.edit_object_data_callback(new_object_name=self.mujoco_app.object_name, new_size=value)
    
    # Pasa el nombre de la esfera 
    def select_sphere(self, value): 
        match value:
            case "Esfera Izquierda":
                value = "left_sphere"
            case "Esfera Derecha":
                value = "right_sphere"
            case _:
                sys.exit("Los nombres de los valores del menu desplegable 'Esferas', o los del xml han sido cambiados. Necesitan ser actualizados")
        self.mujoco_app.edit_object_data_callback(new_size=None, new_object_name=value) # Envia el nuevo nombre

#EJECUTAR PROGRAMA

    # Ejecuta CustomTkinter
    def start_tkinter(self):
        self.app.mainloop()

    # Ejecuta MuJoCo
    def run_mujoco(self): 
        self.mujoco_app = OpenMujoco(960,540,self.xml_path)
        if self.file_exists == True:
            self.read_file()
            
        self.mujoco_app.run()

def main():
    programa = Tkinter_UI("src\\models\\esfera.xml")
    programa.start_tkinter()

if __name__ == "__main__":
    main()