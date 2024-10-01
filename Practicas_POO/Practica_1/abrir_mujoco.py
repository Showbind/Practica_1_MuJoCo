import mujoco as mj
from mujoco.glfw import glfw
import numpy as np

# Resolucion inicial del renderizado
rendering_width = 960
rendering_heigth = 540

#Estado de los botones
mouse_button_left_pressed = False

def open_window_and_start_mujoco(): # Abrir ventana (OpenGL) e Iniciar MuJoCo
    global model, data, camera, opt, scn, context, scene

    # Iniciar glfw (OpenGL API)
    try:
        glfw.init() 
    except:
        raise("Error al iniciar glfw")
    
    # Crear y manejar error ventana
    global window
    window = glfw.create_window(960,540,"MuJoCo: Motor de Fisicas", None, None)

    # Fijar ASPECT RATIO (ej: 16:9) 
    '''glfw.set_window_aspect_ratio(window,16,9)'''
    
    if window == False: # En caso de error
        glfw.terminate()
        glfw.viewport()
        raise("Error al abrir la ventana de la aplicación")
    
    # Establecer el contexto de OpenGL
    glfw.make_context_current(window)
    glfw.swap_interval(1)  # V-Sync (1) = On

    # Mouse callback (llama a mouse_button_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback) # boton izquierdo presionado

    # Window resize callback (llama a window_size_callback)
    glfw.set_window_size_callback(window, window_size_callback)

    # Inicializar variables de MuJoCo
    model = mj.MjModel.from_xml_path("Practicas_POO\Practica_1\cubo.xml") #Cargar Modelo 
    data = mj.MjData(model) # Establecer data para cada modelo
    camera = mj.MjvCamera() # Establecer camera
    opt = mj.MjvOption() # Para las opciones de visualizacion

    # Establecer Escena y Contexto (Inicializacion)
    scene = mj.MjvScene(model, maxgeom=10000) 
    context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value) # Contexto para la GPU
   
    # Tipo de camera y opcion default
    mj.mjv_defaultCamera(camera)
    mj.mjv_defaultOption(opt)

def window_size_callback(window,width,heigth):
    global rendering_width, rendering_heigth

    rendering_width = width
    rendering_heigth = heigth

    print("- Resolucion actual:", "(", width, ",", heigth, ")")

def mouse_button_callback(window, button, action, mods):
    global mouse_button_left_pressed

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
       mouse_button_left_pressed = True
    else:
        mouse_button_left_pressed = False

def main():
    open_window_and_start_mujoco()

    while glfw.window_should_close(window) == False:
        #Render here
        mj.mj_step(model, data)
        mj.mj_forward(model, data)

        # Si boton izq del mouse presionado -> Establecer accion deseada
        if mouse_button_left_pressed == True:
            print("     - Boton izquierdo presionado:",mouse_button_left_pressed) # Accion del boton aqui
        
        # Update de la escena 
        mj.mjv_updateScene(model, data, opt, None, camera, mj.mjtCatBit.mjCAT_ALL.value, scene)        
        # Render de la escena 
        mj.mjr_render(mj.MjrRect(0, 0, rendering_width, rendering_heigth), scene, context)
        # Intercambiar buffers (Velocidad establecida por V-Sync) 
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()