from src.mujoco import CreateMujocoWindow

def main():
    abrir_programa = CreateMujocoWindow(960,540,"Practicas_POO\Practica_1\src\models\cubo.xml")
    abrir_programa.run()

if __name__ == "__main__":
    main()