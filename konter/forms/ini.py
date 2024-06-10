import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import sys
import os
import docker
from docker.errors import APIError

# Añadir el directorio raíz del proyecto al sys.path para importar módulos personalizados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.util_ventana as utl
import utils.util_imagenes as util_img
from forms.form_master import FormularioMaster
from config import COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA

# Función para iniciar sesión en Docker
def docker_login(username, password, email=None, registry='https://index.docker.io/v1/'):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    
    try:
        # Intentar iniciar sesión con las credenciales proporcionadas
        response = client.login(
            username=username,
            password=password,
            email=email,
            registry=registry
        )
        print("Login exitoso:", response)
        return client
    except APIError as e:
        # Capturar errores de la API y devolver None si falla el inicio de sesión
        print(f"Error durante el login: {e}")
        return None

# Clase principal de la aplicación
class App:
    # Método para verificar las credenciales y proceder con el inicio de sesión
    def verificar(self, event=None):
        usu = self.usuario.get()
        password = self.password.get()

        client = docker_login(usu, password)
        if client:
            self.ventana.destroy()  # Cerrar la ventana de inicio de sesión
            FormularioMaster(client).mainloop()  # Abrir el formulario principal
        else:
            # Mostrar mensaje de error si la autenticación falla
            messagebox.showerror(message="La autenticación en Docker Hub falló. Verifique sus credenciales.", title="Mensaje")

    # Constructor de la clase App
    def __init__(self):
        # Configuración de la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title('Inicio de sesión')
        self.ventana.geometry('800x500')
        self.ventana.config(bg=COLOR_CUERPO_PRINCIPAL)
        self.ventana.resizable(width=0, height=0)
        utl.centrar_ventana(self.ventana, 800, 500)

        # Configuración de fuente predeterminada
        self.ventana.option_add('*Font', 'Arial 14')

        # Cargar y mostrar el logo de la aplicación
        logo = util_img.leer_imagen(os.path.join(os.path.dirname(__file__), "../imagenes/konter-logo.png"), (200, 200))
        self.logo = logo  # Mantener una referencia a la imagen para evitar que sea recolectada por el garbage collector

        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg=COLOR_MENU_LATERAL)
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg=COLOR_MENU_LATERAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Configuración del formulario de inicio de sesión
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg=COLOR_CUERPO_PRINCIPAL)
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        
        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg=COLOR_CUERPO_PRINCIPAL)
        frame_form_top.pack(side="top", fill=tk.X)
        
        title = tk.Label(frame_form_top, text='INICIO DE SESIÓN', font=('Monserrat', 20, 'bold'), fg='#394956', bg=COLOR_CUERPO_PRINCIPAL, pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg=COLOR_CUERPO_PRINCIPAL)
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Campo de entrada para el nombre de usuario
        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Monserrat', 14), fg="#666a88", bg=COLOR_CUERPO_PRINCIPAL, anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Arial', 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        # Campo de entrada para la contraseña
        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Monserrat', 14), fg="#666a88", bg=COLOR_CUERPO_PRINCIPAL, anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Monserrat', 14), show="*")
        self.password.pack(fill=tk.X, padx=20, pady=10)

        # Botón para iniciar sesión
        inicio = tk.Button(frame_form_fill, text="Iniciar sesión", font=('Monserrat', 15, BOLD), bg=COLOR_MENU_CURSOR_ENCIMA, bd=0, fg="#fff", command=self.verificar)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", self.verificar)
        
        self.ventana.mainloop()  # Iniciar el bucle principal de la interfaz gráfica
