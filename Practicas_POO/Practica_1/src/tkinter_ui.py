import customtkinter

class App(customtkinter.CTk):
    def __init__(self):   
        super().__init__() 
        
        self.title("MuJoCo: User Interface")
        self.geometry("960x540")
        
#Run       
app = App()
app.mainloop()  