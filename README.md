# MuJoCo Simulador

Se ha implementado una instancia de OpenGL la cual renderizá el motor de físicas MuJoCo. Tanto los parámetros que se pasan como el control del motor son realizados en python.

## Interfaz de Usuario
![tkinter_ui](https://github.com/gabi-er/Practicas_POO/blob/main/images/tkinter_ui.png "MuJoCo User Interface")
 
  ### BOTONES
  - Ejecutar MuJoCo: Inicia la simulación con los ajustes predefinidos.
  - Abrir Archivo: Carga un archivo con los parámetros deseados del usuario (formato .json) (archivos .txt, .json)
  - Menú Desplegable: Permite elegir una de las dos esferas para poder cambiar el tamaño de estas (entre 0 y 0.3)

## Simulación
![tkinter_ui](https://github.com/gabi-er/Practicas_POO/blob/main/images/mujoco_sim_1.gif "Uso de la interfaz y funcionamiento de la simulación")
  
  ### ARCHIVOS
  El programa se encuentra divido en tres archivos principales:
  - main.py : Encargado de ejecutar la interfaz de simulación como tal.
  - mujoco_ui.py : Gestiona toda la interfaz del simulador y todas las llamadas creadas por la interacción entre el usuario y la interfaz con el simulador.
  - mujoco_simulador.py : Crea y gestiona la ventana del simulador, además de iniciar todos los modelados e interacciones físicas de la simulación.