from src.mujoco_ui import Tkinter_UI


def main():
    programa = Tkinter_UI("Practicas_POO\\Practica_1\\src\\models\\esfera.xml")
    programa.start_tkinter()

if __name__ == "__main__":
    main()