from src.mujoco_simulador import OpenMujoco

def main():
    path = "Practicas_POO\Practica_1\src\models\esfera.xml"

    # Ejecutar MuJoCo
    abrir_programa = OpenMujoco(960,540,path) 
    abrir_programa.edit_object_callback("red_sphere", 0.05)
    abrir_programa.run()
    # Editar objetos
    # Ejecutar Programa
    

if __name__ == "__main__":
    main()