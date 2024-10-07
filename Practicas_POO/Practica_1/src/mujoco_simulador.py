import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import glfw

class openMujoco: # Abrir ventana (OpenGL) e Iniciar MuJoCo
    def __init__(self,initial_width,initial_heigth,path): 
        # Resolucion inicial del renderizado
        self.rendering_width = initial_width
        self.rendering_heigth = initial_heigth

        #Estado de los botones
        self.mouse_button_left_pressed = False

        # Iniciar glfw (OpenGL API)
        try:
            glfw.init() 
        except:
            raise("Error al iniciar glfw")
        
        # Crear y manejar error ventana
        self.window = glfw.create_window(initial_width,initial_heigth,"MuJoCo: Motor de Fisicas", None, None)

        # Fijar ASPECT RATIO (ej: 16:9) 
            #glfw.set_window_aspect_ratio(window,16,9)
        
        if self.window == False: # En caso de error
            glfw.terminate()
            glfw.viewport()
            raise("Error al abrir la ventana de la aplicación")
        
        # Establecer el contexto de OpenGL
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # V-Sync (1) = On

        # Mouse callback (llama a mouse_button_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback) # boton izquierdo presionado

        # Window resize callback (llama a window_size_callback)
        glfw.set_window_size_callback(self.window, self.window_size_callback)

        # Inicializar variables de MuJoCo
        self.model = mj.MjModel.from_xml_path(path) #Cargar Modelo 
        self.data = mj.MjData(self.model) # Establecer data para cada modelo
        self.camera = mj.MjvCamera() # Establecer camera
        self.opt = mj.MjvOption() # Para las opciones de visualizacion

        # Establecer Escena y Contexto (Inicializacion)
        self.scene = mj.MjvScene(self.model, maxgeom=10000) 
        self.context = mj.MjrContext(self.model, mj.mjtFontScale.mjFONTSCALE_150.value) # Contexto para la GPU
    
        # Tipo de camera y opcion default
        mj.mjv_defaultCamera(self.camera)
        mj.mjv_defaultOption(self.opt)

    def window_size_callback(self,window,width,heigth):
        global rendering_width, rendering_heigth

        self.rendering_width = width
        self.rendering_heigth = heigth

        print("- Resolucion actual:", "(", width, ",", heigth, ")") 

    def mouse_button_callback(self,window, button, action, mods):
        global mouse_button_left_pressed
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            self.mouse_button_left_pressed = True
        else:
            self.mouse_button_left_pressed = False

    def run(self,path): # Ejecuta MuJoCo después de abrir la ventana
            
        while glfw.window_should_close(self.window) == False:
            #Render here
            mj.mj_step(self.model, self.data)
            mj.mj_forward(self.model, self.data)

            # Si boton izq del mouse presionado -> Establecer accion deseada
            if self.mouse_button_left_pressed == True:
                # Accion del boton aqui
                print("     - Boton izquierdo presionado:",self.mouse_button_left_pressed) 

                # Vuelve a cargar el objeto (Para actualizar el objeto desde la UI)
                self.model = mj.MjModel.from_xml_path(path) 

            # Update de la escena 
            mj.mjv_updateScene(self.model, self.data, self.opt, None, self.camera, mj.mjtCatBit.mjCAT_ALL.value, self.scene)  

            # Render de la escena 
            mj.mjr_render(mj.MjrRect(0, 0, self.rendering_width, self.rendering_heigth), self.scene, self.context)

            # Intercambiar buffers (Velocidad establecida por V-Sync) 
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            
        glfw.terminate()

def main():
    simulador = openMujoco(960,540, "Practicas_POO\Practica_1\src\models\cubo.xml")
    simulador.run()

if __name__ == "__main__":
    main()