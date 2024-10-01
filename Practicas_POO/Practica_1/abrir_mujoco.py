import mujoco as mj
from mujoco.glfw import glfw
import numpy as np

def open_window_and_start_mujoco(): # Iniciar OpenGL
    global model, data, camera, opt, scn, context, scene
    try:
        glfw.init()
    except:
        raise("Error al iniciar glfw")
    
    # Crear y manejar error ventana
    global window
    window = glfw.create_window(960,540,"MuJoCo: Motor de Fisicas", None, None)
    
    if window == False:  
        glfw.terminate()
        glfw.viewport()
        
        raise("Error al abrir la ventana de la aplicación")
    
    # Establecer el contexto de OpenGL
    glfw.make_context_current(window)
    glfw.swap_interval(1)  # V-Sync (1) = On

    # Llamada de raton y teclado

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

def main():
    open_window_and_start_mujoco()

    while glfw.window_should_close(window) == False:
        #Render here
        mj.mj_step(model, data)
        mj.mj_forward(model, data)

        # Update de la escena 
        mj.mjv_updateScene(model, data, opt, None, camera, mj.mjtCatBit.mjCAT_ALL.value, scene)

        # Actualizacion del tamaño del render según el usuario re-escala la ventana
        rendering_width = glfw.get_framebuffer_size(window)[0]
        rendering_heigth = glfw.get_framebuffer_size(window)[1]

        # Render de la escena 
        mj.mjr_render(mj.MjrRect(0, 0, rendering_width, rendering_heigth), scene, context)

        # Intercambiar buffers (Velocidad establecida por V-Sync) 
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()