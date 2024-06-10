
import sys
import os

#El main.py es el que incia la aplicación 
#Con este sys.path me aseguro que el main.py encuentre los directorios o modulos nececesarios
#dentro del mismo directorio que main.py

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from forms.form_login import App

if __name__ == "__main__":
    App()  
