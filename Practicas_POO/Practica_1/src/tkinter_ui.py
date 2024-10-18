import customtkinter
import threading
from mujoco_simulador import openMujoco

# Modo Interfaz
customtkinter.set_appearance_mode("dark")

# Estado del hilo
thread_is_running = False

# Path del objeto de MuJoCo
xml_path = "Practicas_POO\Practica_1\src\models\esfera.xml"

# Inicialización del objeto
mujoco_executable = None

# Callbacks
def slider_event(value): # Cambia el tamaño de la esfera
    global size
    size = value
    mujoco_executable.update_object_size(size)

def run_mujoco(): # Ejecuta la simulacion
    global mujoco_executable
    mujoco_executable = openMujoco(960,540,xml_path)
   # mujoco_executable.size = size
    mujoco_executable.run()

def button_run_mujoco(): # Run simulador
    global thread_is_running
    if thread_is_running == False: # Ejecuta MuJoCo
        thread_is_running = True
        threading.Thread(target=run_mujoco, daemon= True).start()
    else:
        print("Ya hay iniciada una instancia de MuJoCo")



# main windows
app = customtkinter.CTk()
app.title("tinker")
app.geometry("1280x720")
#root.bind("<Return>", on_enter_ke

# configure grid layout (4x4)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0, 1, 2), weight=1)

#-----------------------------------------------------------
# create sidebar frame with widgets
#-----------------------------------------------------------
sidebar_frame = customtkinter.CTkFrame(master=app, width=20, corner_radius=0)
sidebar_frame.grid(row=1, column=0, padx=20, pady=2, rowspan=1, columnspan=1, sticky="w")
sidebar_frame.grid_rowconfigure(4, weight=1)

slider_pos = customtkinter.CTkSlider(master=app, from_=0.1, to=2, command=slider_event)
slider_pos.grid(row=3, column=3, padx=10, pady=5, sticky="w")

button_1 = customtkinter.CTkButton(master=app, command=button_run_mujoco)
button_1.grid(row=10, column=3, padx=10, pady=5, sticky="w")

app.mainloop()
