import mujoco as mj
from mujoco.glfw import glfw
import numpy as np



def open_window(): # Iniciar OpenGL
    try:
        glfw.init()
    except:
        raise("Error al iniciar glfw")
    
    # Crear y manejar error ventana
    global window
    window = glfw.create_window(960,540,"MuJoCo: Motor de Fisicas", None, None) 
    
    if window == False:  
        glfw.terminate()
        raise("Error al abrir la ventana de la aplicación")
    
    # Establecer el contexto de OpenGL
    glfw.make_context_current(window)
    glfw.swap_interval(1)  # V-Sync (1) = On
def mouse():
    glfw.set_cursor_pos_callback(window)
   
def main():
    open_window()
    while glfw.window_should_close(window) == False:
        #Render here
        mouse()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    



if __name__ == "__main__":
    main()