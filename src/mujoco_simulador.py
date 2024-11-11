import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import glfw
import numpy as np
from scipy.spatial.transform import Rotation as R

class OpenMujoco: # Abrir ventana (OpenGL) e Iniciar MuJoCo
    def __init__(self,initial_width:int,initial_heigth:int,xml_path): 

        # Resolucion Inicial renderizado
        self.rendering_width = initial_width
        self.rendering_heigth = initial_heigth
        self.xml_path = xml_path

        # Raton                                  
        self.scroll_offset = 2 # Valor inicial distancia cámara
        self.mouse_scroll_changed = False

    #PROPIEDADES ESFERA

        # Tamaño ESFERA
        self.size = None
        self.old_size = self.size

        # Nombre del objeto
        self.object_name = "left_sphere"

        #Estado de los botones
        self.mouse_button_right_pressed = False

        # Iniciar glfw (OpenGL API)
        try:
            glfw.init() 
        except:
            raise("Error al iniciar glfw")
        
        # Crear y manejar error ventana
        self.window = glfw.create_window(initial_width,initial_heigth,"MuJoCo: Motor de Fisicas", None, None)

        # Fijar Aspect Ratio (ej: 16:9) 
            #glfw.set_window_aspect_ratio(window,16,9)
        
        if self.window == False: # En caso de error
            glfw.terminate()
            glfw.viewport()
            raise("Error al abrir la ventana de la aplicación")
        
        # Establecer el contexto de OpenGL
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # V-Sync (1) = On

    # LLAMADA A CALLBACKS

        # Si mouse_right_button_pressed == True
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback) 
        glfw.set_cursor_pos_callback(self.window, self.mouse_position_callback)

        # Scroll mouse
        glfw.set_scroll_callback(self.window,self.mouse_scroll_callback)

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
        self.camera.distance = self.scroll_offset
        mj.mjv_defaultOption(self.opt) 

# HIGH-ORDER FUNCTIONS
    
    def if_sphere_size_changed(self): # Detecta y cambia el nuevo tamaño de la esfera
        if self.size != self.old_size:  
               self.update_object_data_callback(body_size=self.size)
               self.old_size = self.size
    
    def if_mouse_button_right_pressed(self):
        if self.mouse_button_right_pressed == True:
                # Accion del boton
                print("     - Boton derecho presionado:",self.mouse_button_right_pressed)

                self.camera.azimuth = -mouse_x/20
                self.camera.elevation = mouse_y/20
    
                print(f"-Posicion raton  x: {mouse_x};   y: {mouse_y}")
    
    def if_mouse_scroll_moved(self): # Cambiar distancia camara
        if self.mouse_scroll_changed == True:
            self.camera.distance = self.scroll_offset
            self.mouse_scroll_changed = False

            print("Scroll Raton Valor:",self.scroll_offset)

# CALLBACKS
    def set_json_object_properties(self,json_dictionary:(dict)=None): # Carga los valores del JSON en el simulador

        # IDs "left_sphere"
        left_sphere_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "left_sphere")
        left_sphere_joint_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "left_sphere_joint")

        # IDs "right_sphere"
        right_sphere_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "right_sphere")
        left_sphere_joint_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "right_sphere_joint")
        
        # IDs rampas
        left_ramp_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "left_ramp")
        right_ramp_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "right_ramp")

        # Atributos "left_sphere"
        self.model.geom_size[left_sphere_id]=json_dictionary["left_sphere"]["size"]
        self.model.geom_rgba[left_sphere_id]=json_dictionary["left_sphere"]["rgba"]
        self.model.body_mass[left_sphere_id]=json_dictionary["left_sphere"]["mass"]
        left_joint_pos_index = self.model.jnt_qposadr[left_sphere_joint_id] # Devuelve el indice del primer eje de coordenadas(x,y,z) del joint 
        self.data.qpos[left_joint_pos_index:left_joint_pos_index+3] = json_dictionary["left_sphere"]["position"] # Cambia los valores de x,y,z del joint 

        # Atributos "right_sphere"
        self.model.geom_size[right_sphere_id]=json_dictionary["right_sphere"]["size"]
        self.model.geom_rgba[right_sphere_id]=json_dictionary["right_sphere"]["rgba"]
        self.model.body_mass[right_sphere_id]=json_dictionary["right_sphere"]["mass"]
        right_joint_pos_index = self.model.jnt_qposadr[left_sphere_joint_id] # Devuelve el indice del primer eje de coordenadas(x,y,z) del joint
        self.data.qpos[right_joint_pos_index:right_joint_pos_index+3] = json_dictionary["right_sphere"]["position"] # Cambia los valores de x,y,z del joint 

        # Atributos "left_ramp"
        #self.model.body_quat[left_ramp_id]=json_dictionary["left_ramp"]["tilt"] # Hay que hacer operaciones con los quaterniones para solo rotar y no mover la rampa de posicion
        #self.model.geom_size[left_ramp_id]=json_dictionary["left_ramp"]["length"]
        #self.model.geom_friction[left_ramp_id]=json_dictionary["left_ramp"]["friction"]
        
        #euler_angles = 567  # Ejemplo: rotación de 90 grados en Z
        #rotation = R.from_euler('y', euler_angles, degrees=False)
        #quat = rotation.as_quat()  # Convertimos a cuaternión
        #self.model.body_pos[left_ramp_id] = [-1, 0.5, -0.3] 
        
        #self.model.body_quat[right_ramp_id]=json_dictionary["right_ramp"]["tilt"] # Hay que hacer operaciones con los quaterniones para solo rotar y no mover la rampa de posicion
        self.model.geom_size[right_ramp_id]=json_dictionary["right_ramp"]["length"]
        self.model.geom_friction[right_ramp_id]=json_dictionary["right_ramp"]["friction"]

    def window_size_callback(self,window,width:int,heigth:int): # Asigna nuevos valores del renderizado de la ventana
        global rendering_width, rendering_heigth

        self.rendering_width = width
        self.rendering_heigth = heigth

        print(f"- Resolucion actual: {width}, {heigth}") 

    def mouse_scroll_callback(self, window, xoffset: float, yoffset: float): # Asigna valor scroll raton
        self.scroll_offset = self.scroll_offset-(yoffset/5)
        self.mouse_scroll_changed = True

    def mouse_position_callback(self, window, xpos:float, ypos:float): # Asigna valores posicion puntero del raton
        global mouse_x, mouse_y
        mouse_x = xpos
        mouse_y = ypos

    def mouse_button_callback(self,window, button, action, mods): # Booleano del click izq del mouse
        global mouse_button_right_pressed
        if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
            self.mouse_button_right_pressed = True
        else:
            self.mouse_button_right_pressed = False

    def update_object_data_callback(self,body_size:int = None): # Actualiza las propiedades del objeto
        object_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, self.object_name)  # Obtener id del objeto según el nombre

        if body_size != None:
            self.model.geom_size[object_id] = body_size # Asignar nuevo tamaño

    def edit_object_data_callback (self, new_object_name:str, new_size:float = None): # Actualiza uno o varios atributos del objeto
        self.object_name = new_object_name
        
        if new_size != None:
            self.size = new_size

# RUNTIME

    # Ejecuta MuJoCo después de abrir la ventana
    def run(self): 
            
        while glfw.window_should_close(self.window) == False:
            #Renderizado
            mj.mj_step(self.model, self.data)
            mj.mj_forward(self.model, self.data)

            # Accion boton derecho raton -> MOVER CAMARA
            self.if_mouse_button_right_pressed()
            self.if_mouse_scroll_moved()
            # Update de la escena 
            mj.mjv_updateScene(self.model, self.data, self.opt, None, self.camera, mj.mjtCatBit.mjCAT_ALL.value, self.scene)

            # Cambiar tamaño esfera
            self.if_sphere_size_changed()
            # Render de la escena 
            mj.mjr_render(mj.MjrRect(0, 0, self.rendering_width, self.rendering_heigth), self.scene, self.context)

            # Intercambiar buffers (Velocidad establecida por V-Sync) 
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            
        glfw.terminate()

def main():
    simulador = OpenMujoco(960,540, "src\models\esfera.xml")
    simulador.run()
   

if __name__ == "__main__":
    main()