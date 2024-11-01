import sys
import ui
import menu

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]== "-t":
        menu.iniciar() #iniciaremos el menu para la terminal
    else:
        app = ui.MainWindow()    
        app.mainloop()
    