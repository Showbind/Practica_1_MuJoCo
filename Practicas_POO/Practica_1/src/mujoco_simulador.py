import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import glfw

class OpenMujoco: # Abrir ventana (OpenGL) e Iniciar MuJoCo
    def __init__(self,initial_width,initial_heigth,xml_path): 

        # Resolucion Inicial renderizado
        self.rendering_width = initial_width
        self.rendering_heigth = initial_heigth
        
        # Tamaño objeto
        self.size = None
        self.old_size = self.size

        # Nombre del objeto
        self.object_name = "red_sphere"

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

        # LLAMADA A CALLBACKS

        # if mouse_left_button_pressed
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback) 

        # if window has been resized
        glfw.set_window_size_callback(self.window, self.window_size_callback) 

        # INICIALIZACION VARIABLES MUJOCO    

        # Establecer variables
        self.model = mj.MjModel.from_xml_path(xml_path) #Cargar Modelo 
        self.data = mj.MjData(self.model) # Establecer data para cada modelo
        self.camera = mj.MjvCamera() # Establecer camera
        self.opt = mj.MjvOption() # Para las opciones de visualizacion

        # Establecer Escena y Contexto 
        self.scene = mj.MjvScene(self.model, maxgeom=10000) # Escena
        self.context = mj.MjrContext(self.model, mj.mjtFontScale.mjFONTSCALE_150.value) # Contexto para la GPU
    
        # Tipo de camera y opcion default
        mj.mjv_defaultCamera(self.camera)
        mj.mjv_defaultOption(self.opt) 

    # CALLBACKS

    def window_size_callback(self,window,width,heigth): # Cambia el tamaño de la ventana
        global rendering_width, rendering_heigth

        self.rendering_width = width
        self.rendering_heigth = heigth

        print(f"- Resolucion actual: {width}, {heigth}") 

    def mouse_button_callback(self,window, button, action, mods): # Booleano del click izq del mouse
        global mouse_button_left_pressed
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            self.mouse_button_left_pressed = True
        else:
            self.mouse_button_left_pressed = False

    def edit_object_callback(self,body_size, body_pos = 0, body_mass = 0): # Actualiza las propiedades del objeto
        object_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, self.object_name)  # Obtener id del objeto según el nombre
        self.model.geom_size[object_id] = body_size # Asignar nuevo tamaño

        print(f"Se ha editado el modelo {body_size}")

    def update_object_properties(self,new_size, new_object_name): # Actualiza uno o varios atributos del objeto
        if new_size != None:
            self.size = new_size

        self.object_name = new_object_name

    # RUNTIME

    # Ejecuta MuJoCo después de abrir la ventana
    def run(self): 
            
        while glfw.window_should_close(self.window) == False:
            #Renderizado
            mj.mj_step(self.model, self.data)
            mj.mj_forward(self.model, self.data)

            # Si boton izq del mouse presionado -> Establecer accion deseada
            if self.mouse_button_left_pressed == True:
                # Accion del boton aqui
                print("     - Boton izquierdo presionado:",self.mouse_button_left_pressed) 

            # Update de la escena 
            mj.mjv_updateScene(self.model, self.data, self.opt, None, self.camera, mj.mjtCatBit.mjCAT_ALL.value, self.scene)

            # Detecta y cambia el nuevo tamaño de la esfera
            if self.size != self.old_size:  
               self.edit_object_callback(self.size)
               self.old_size = self.size

            # Render de la escena 
            mj.mjr_render(mj.MjrRect(0, 0, self.rendering_width, self.rendering_heigth), self.scene, self.context)

            # Intercambiar buffers (Velocidad establecida por V-Sync) 
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            
        glfw.terminate()

def main():
    simulador = OpenMujoco(960,540, "Practicas_POO\Practica_1\src\models\esfera.xml")
    simulador.run()
   

if __name__ == "__main__":
    main()