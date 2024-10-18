from src.mujoco_simulador import openMujoco

def main():
    path = "Practicas_POO\Practica_1\src\models\esfera.xml"

    # Ejecutar MuJoCo
    abrir_programa = openMujoco(960,540,path) 
    abrir_programa.edit_objects("red_sphere", 0.1)
    abrir_programa.run()
    # Editar objetos
    # Ejecutar Programa
    

if __name__ == "__main__":
    main()