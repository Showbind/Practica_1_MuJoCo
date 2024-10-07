from src.mujoco_simulador import openMujoco

def main():
    path = "Practicas_POO\Practica_1\src\models\cubo.xml"

    # Ejecutar MuJoCo
    abrir_programa = openMujoco(960,540,path) 
    abrir_programa.run(path)

if __name__ == "__main__":
    main()