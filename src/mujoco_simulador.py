import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import glfw
import numpy as np
from scipy.spatial.transform import Rotation as R

class OpenMujoco: # Abrir ventana (OpenGL) e Iniciar MuJoCo
    def __init__(self,initial_width:int,initial_heigth:int,xml_path): 

    # PROPIEDADES RENDERIZADO

        # Resolucion Inicial renderizado
        self.rendering_width = initial_width
        self.rendering_heigth = initial_heigth

        self.xml_path = xml_path

    # PROPIEDADES RATON

        # Scroll     
        self.mouse_scroll_changed = False                             
        self.scroll_offset = 2 

        # Puntero raton
        self.mouse_old_x = 0 
        self.mouse_old_y = 0

        # Estado de los botones
        self.mouse_button_right_pressed = False

    # PROPIEDADES CAMARA

        # Desplazamiento Angular
        self.old_camera_azimuth = 90
        self.old_camera_elevation = -45

    # PROPIEDADES ESFERA

        # Tamaño ESFERA
        self.size = None
        self.old_size = self.size

        self.sphere_name = "left_sphere" 

    # PROPIEDADES RAMPA

        # Inclinacion Rampa
        self.tilt = None
        self.old_tilt = self.tilt

        self.ramp_name = "left_ramp"

    # INICIAR GLFW (OpenGL API)

        try:
            glfw.init() 
        except:
            raise("Error al iniciar glfw")
        
        # Crear y manejar error ventana
        self.window = glfw.create_window(initial_width,initial_heigth,"MuJoCo: Motor de Fisicas", None, None)

        # Fijar Aspect Ratio (ej: 16:9) (OPCIONAL)
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
               self.update_sphere_size_callback(sphere_size=self.size)
               self.old_size = self.size

    def if_ramp_tilt_changed(self): # Detecta y cambia la nueva inclinación de la rampa
        if self.tilt != self.old_tilt:
            self.change_ramp_tilt_callback()
            self.old_tilt = self.tilt

    def if_mouse_button_right_pressed(self):
        if self.mouse_button_right_pressed == True:
                # Girar Camara
                self.camera.azimuth = self.old_camera_azimuth-(mouse_x-self.mouse_old_x)*0.5
                self.camera.elevation = self.old_camera_elevation-(mouse_y-self.mouse_old_y)*0.5
    
                print(f"-Posicion raton  x: {mouse_x};   y: {mouse_y}")
    
    def if_mouse_scroll_moved(self): # Cambiar distancia camara
        if self.mouse_scroll_changed == True:
            self.camera.distance = self.scroll_offset
            self.mouse_scroll_changed = False

            print("Scroll Raton Valor:",self.scroll_offset)

# CALLBACKS

    def set_json_object_properties(self,json_dictionary:dict=None): # Carga los valores del JSON en el simulador
    # IDs

        # IDs "left_sphere"
        left_sphere_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "left_sphere")
        left_sphere_joint_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "left_sphere_joint")

        # IDs "right_sphere"
        right_sphere_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "right_sphere")
        right_sphere_joint_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "right_sphere_joint")
        
        # IDs rampas
        left_ramp_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "left_ramp")
        right_ramp_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, "right_ramp")

    # ESFERAS

        # Atributos "left_sphere"
        self.model.geom_size[left_sphere_id]=json_dictionary["left_sphere"]["size"] # Tamaño
        self.model.geom_rgba[left_sphere_id]=json_dictionary["left_sphere"]["rgba"] # Color
        self.model.body_mass[left_sphere_joint_id]=json_dictionary["left_sphere"]["mass"] # Masa
        left_joint_pos_index = self.model.jnt_qposadr[left_sphere_joint_id] # Puntero de la posiciones (x,y,z) del joint
        self.data.qpos[left_joint_pos_index:left_joint_pos_index+3] = json_dictionary["left_sphere"]["position"] # Cambia la posicion del objeto asociado al joint (x,y,z)

        # Atributos "right_sphere"
        self.model.geom_size[right_sphere_id]=json_dictionary["right_sphere"]["size"] # Tamaño
        self.model.geom_rgba[right_sphere_id]=json_dictionary["right_sphere"]["rgba"] # Color
        self.model.body_mass[right_sphere_joint_id]=json_dictionary["right_sphere"]["mass"] # Masa
        right_joint_pos_index = self.model.jnt_qposadr[right_sphere_joint_id] # Puntero de la posiciones (x,y,z) del joint
        self.data.qpos[right_joint_pos_index:right_joint_pos_index+3] = json_dictionary["right_sphere"]["position"] # Cambia la posicion del objeto asociado al joint (x,y,z)

    # RAMPAS

        # Calculo Cuaternion
        w = lambda angle:np.cos(angle/2)
        y = lambda angle:np.sin(angle/2)
         
        # Atributos "left_ramp"
        tilt_angle = -2*3.14*(json_dictionary["left_ramp"]["tilt"])/360 # Extraer angulo inclinacion

        self.model.geom_quat[left_ramp_id] = [w(tilt_angle),0,y(tilt_angle),0] # Inclinacion
        self.model.geom_size[left_ramp_id]=json_dictionary["left_ramp"]["length"] # Longitud
        self.model.geom_friction[left_ramp_id]=json_dictionary["left_ramp"]["friction"] # Friccion
        
        # Atributos "right_ramp"
        tilt_angle = -2*3.14*(json_dictionary["right_ramp"]["tilt"])/360 # Extraer angulo inclinacion

        self.model.geom_quat[right_ramp_id] = [w(tilt_angle),0,y(tilt_angle),0] # Inclinacion
        self.model.geom_size[right_ramp_id]=json_dictionary["right_ramp"]["length"] # Longitud
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
        if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS: # Si se presiona el boton
            self.mouse_old_x = mouse_x
            self.mouse_old_y = mouse_y
            self.mouse_button_right_pressed = True
        elif button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.RELEASE: # Si se suelta el boton
            self.old_camera_azimuth = self.camera.azimuth
            self.old_camera_elevation = self.camera.elevation
            self.mouse_button_right_pressed = False
        else: # Si no esta presionado
            self.mouse_button_right_pressed = False

    def update_sphere_size_callback(self,sphere_size:int = None): # Actualiza el tamaño de la esfera
        self.sphere_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, self.sphere_name)  # Obtener id del objeto según el nombre

        if sphere_size != None:
            self.model.geom_size[self.sphere_id] = sphere_size # Asignar nuevo tamaño

    def change_ramp_tilt_callback(self): # Cambia el valor de la inclinación de la rampa
        ramp_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, self.ramp_name)

        w = np.cos(self.tilt/2)
        y = np.sin(self.tilt/2)
        cuaternion = [w,0,y,0]
        self.model.geom_quat[ramp_id] = cuaternion

    def edit_object_data_callback (self, new_sphere_name:str = None, new_ramp_name:str = None, new_size:float = None, new_tilt:float = None): # Actualiza uno o varios atributos del objeto
        if new_sphere_name != None:
            self.sphere_name = new_sphere_name

        if new_size != None:
            self.size = new_size

        if new_ramp_name != None:
            self.ramp_name = new_ramp_name
        
        if new_tilt != None:
            self.tilt = new_tilt

# RUNTIME

    # Ejecuta MuJoCo después de abrir la ventana
    def run(self): 
            
        while glfw.window_should_close(self.window) == False:
            #Renderizado
            mj.mj_step(self.model, self.data)
            mj.mj_forward(self.model, self.data)

            # Cambiar Posicion Camara
            self.if_mouse_button_right_pressed()
            self.if_mouse_scroll_moved()

            # Cambiar Tamaño Esfera
            self.if_sphere_size_changed()

            # Cambiar Inclinacion Rampa
            self.if_ramp_tilt_changed()
            
            # Update de la escena 
            mj.mjv_updateScene(self.model, self.data, self.opt, None, self.camera, mj.mjtCatBit.mjCAT_ALL.value, self.scene)
            
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