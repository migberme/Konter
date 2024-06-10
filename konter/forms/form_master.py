import tkinter as tk
from tkinter import font, simpledialog, messagebox
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import utils.util_imagenes as util_img
import utils.util_ventana as util_ventana
import docker
from docker.errors import APIError, ImageNotFound, NotFound
import os
import subprocess
import time

"""
Con class creamos el objeto FormularioMaster y con (tk.Tk) invoco todos 
los componentes de tk para poder utilizarlos
"""
class FormularioMaster(tk.Tk):

    # Con la función / método init
    def __init__(self, client):
        # como voy a heredar el objeto tk.Tk utilizo la palabra reservada super() e invoco su constructor .__init__()
        super().__init__()
        # En self.logo guardo la info de la carpeta utils utilizando la función de leer imagen
        self.client = client
        self.logo = util_img.leer_imagen("./imagenes/konter-logo.png", (560, 136))
        self.perfil = util_img.leer_imagen("./imagenes/konter-logo.png", (100, 100))
        self.menu_icon = util_img.leer_imagen("./imagenes/menu-icon2.png", (50, 50))
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.control_menu_lateral()

    # Este método será para la configuración de la ventana
    def config_window(self):
        # configuración inicial de la ventana
        self.title('Konter')
        self.icon_image = tk.PhotoImage(file="./imagenes/konter-logo.png")
        # Con esto indico el tamaño que tendrá la ventana
        w, h = 400, 750
        # Invoco la función de centrar la ventana.
        util_ventana.centrar_ventana(self, w, h)

    # Con esta función voy a distribuir las secciones del menú
    def paneles(self):
        # Creando los paneles de barra superior, menú lateral
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        # con el .pack le digo la forma de como guardarlo, diciéndole con tk.Top que lo guarde en la parte superior
        self.barra_superior.pack(side=tk.TOP, fill='both')

        # Ahora el panel para el menú de la izquierda:
        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=200)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=True)

    def controles_barra_superior(self):
        font_symbola = font.Font(family='Symbola', size=12)

        # Etiqueta para el título
        self.labelTitulo = tk.Label(self.barra_superior, text="Konter")
        self.labelTitulo.config(fg="#fff", font=("Monserrat", 15, 'bold'), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)


        # Etiqueta de información
        self.labelTitulo = tk.Label(self.barra_superior, text="@konterhub")
        self.labelTitulo.config(fg="#fff", font=("Monserrat", 12, 'bold'), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)

    # Configuración del menú lateral
    def control_menu_lateral(self):
        ancho_menu = 25
        alto_menu = 2
        font_symbola = font.Font(family='Symbola', size=15)
        font_roboto = font.Font(family='Monserrat', size=12)

        # Etiqueta del perfil
        self.labelPeril = tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPeril.pack(side=tk.TOP, pady=10)

        # Botones del menú lateral
        self.botonListarContenedor = tk.Button(self.menu_lateral)
        self.botonCrearIniciarContenedor = tk.Button(self.menu_lateral)
        self.botonPararContenedor = tk.Button(self.menu_lateral)
        self.botonIniciarContenedor = tk.Button(self.menu_lateral)
        self.botonEliminarContenedor = tk.Button(self.menu_lateral)
        self.botonListarImagenes = tk.Button(self.menu_lateral)
        self.botonCrearImagenes = tk.Button(self.menu_lateral)
        self.botonEliminarImagenes = tk.Button(self.menu_lateral)
        self.botonEntrarConsola = tk.Button(self.menu_lateral) 


        botones_info = [
            ("Listar Contenedores", "\u2b07", self.listar_contenedores, self.botonListarContenedor),
            ("Crear Contenedor", "\u2795", self.crear_y_correr_contenedor, self.botonCrearIniciarContenedor),
            ("Parar Contenedor", "\u23F9",  self.parar_contenedor, self.botonPararContenedor),
            ("Iniciar Contenedor", "\u25B6",  self.iniciar_contenedor, self.botonIniciarContenedor),
            ("Eliminar Contenedor", "\u274e", self.eliminar_contenedor, self.botonEliminarContenedor),
            ("Listar Imágenes", "\u2b07", self.listar_imagenes, self.botonListarImagenes),
            ("Construir Imagen", "\u2692", self.construir_imagen, self.botonCrearImagenes),
            ("Eliminar Imagen", "\u274C", self.eliminar_imagen, self.botonEliminarImagenes),
            ("Entrar Consola", "\u2318", self.entrar_consola, self.botonEntrarConsola)
        ]

        # Ahora genero un bucle for que recorra los elementos de buttons_info
        for text, icon, command, boton in botones_info:
            boton.config(text=f"{icon}    {text}", anchor="w", font=font_roboto,
                         bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu, command=command)
            boton.pack(side=tk.TOP)
            self.bind_hover_events(boton)

    def config_boton_menu(self, text, icon, boton, font_roboto, ancho_menu, alto_menu):
        boton.config(text=f"{icon}    {text}", anchor="w", font=font_roboto,
                     bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
        boton.pack(side=tk.TOP)
        self.bind_hover_events(boton)

    def bind_hover_events(self, boton):
        # Asociar eventos enter y leave con la función dinámica
        boton.bind("<Enter>", lambda event: self.on_entrar(event, boton))
        boton.bind("<Leave>", lambda event: self.on_cerrar(event, boton))

    def on_entrar(self, event, boton):
        boton.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg="white")

    def on_cerrar(self, event, boton):
        boton.config(bg=COLOR_MENU_LATERAL, fg="white")

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    # Funciones de administración de Docker, este es el mismo código que en la fase 2 pero llevado a funciones
    # Hubiera estado bien que estuviera en otra carpeta para tenerlo más a mano pero por cuestiones de tiempo
    # Como funiciona y hace lo que tiene que hacer, aquí se a quedeado 
    def listar_contenedores(self):
        try:
            contenedores = self.client.containers.list(all=True)

            if not contenedores:
                messagebox.showinfo("Información", "No se encontraron contenedores.")
                return

            info_contenedores = ""
            for contenedor in contenedores:
                info_contenedores += f"ID: {contenedor.id}\nNombre: {contenedor.name}\nEstado: {contenedor.status}\n\n"
                print(f"ID: {contenedor.id} Nombre: {contenedor.name}, Estado: {contenedor.status}")

        except APIError as e:
            messagebox.showerror("Error", f"Ha ocurrido un error con la API de Docker: {e}")
        except NotFound:
            messagebox.showerror("Error", "No se encontró el demonio de Docker. Asegúrate de que Docker está instalado y ejecutándose.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")
    
    def crear_y_correr_contenedor(self):
        imagen = simpledialog.askstring("Imagen de Docker", "Ingrese el nombre de la imagen de Docker:")
        if not imagen:
            print("No se proporcionó una imagen.")
            return

        nombre_contenedor = simpledialog.askstring("Nombre del Contenedor", "Ingrese el nombre del contenedor:")
        if not nombre_contenedor:
            print("No se proporcionó un nombre para el contenedor.")
            return

        try:
            # Crear un contenedor sin iniciarlo
            container = self.client.containers.create(image=imagen, command='tail -f /dev/null', name=nombre_contenedor)
            print(f"Contenedor {nombre_contenedor} ha sido creado y su ID es: {container.id}")

            container.reload()  # Recarga los datos del contenedor
            estado = container.status  # Obtener el estado del contenedor directamente
            print(f"Estado del contenedor {nombre_contenedor}: {estado}")

            container.start()  # Inicia el contenedor
            container.reload()
            estado = container.status  # Obtener el estado del contenedor directamente
            print(f"Estado del contenedor {nombre_contenedor}: {estado}")

            messagebox.showinfo("Éxito", f"El contenedor '{nombre_contenedor}' ha sido creado y está en estado '{estado}'.")

        except ImageNotFound:
            messagebox.showerror("Error", f"La imagen '{imagen}' no fue encontrada. Por favor, asegúrate de que el nombre de la imagen es correcto y que la imagen existe.")
        except APIError as e:
            messagebox.showerror("Error", f"Ha ocurrido un error con la API de Docker: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")

    def parar_contenedor (self):
            nombre_o_id = simpledialog.askstring("Parar Contenedor", "Introduce el nombre o ID del contenedor para detener:")
            if not nombre_o_id:
                messagebox.showerror("Error", "No se proporcionó un nombre o ID de contenedor.")
                return

            try:
                container = self.client.containers.get(nombre_o_id)
                
                container.reload()
                estado = container.status
                print(f"Estado actual del contenedor {nombre_o_id}: {estado}")

                if estado == 'running':
                    print ("Esta operacion puede tardar unos segundos...")
                    container.stop(timeout=2)
                    container.reload()
                    estado = container.status
                    print(f"Contenedor {nombre_o_id} detenido. Estado actual: {estado}")
                    messagebox.showinfo("Éxito", f"El contenedor '{nombre_o_id}' ha sido detenido. Estado actual: {estado}.")
                else:
                    messagebox.showinfo("Información", f"El contenedor '{nombre_o_id}' no está en ejecución (estado: {estado}).")

            except NotFound:
                messagebox.showerror("Error", f"El contenedor con nombre o ID '{nombre_o_id}' no fue encontrado.")
            except APIError as e:
                messagebox.showerror("Error", f"Error en la API de Docker: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")
    
    def iniciar_contenedor(self):
        nombre_o_id = simpledialog.askstring("Iniciar Contenedor", "Introduce el nombre o ID del contenedor que deseas iniciar:")
        if not nombre_o_id:
            messagebox.showerror("Error", "No se proporcionó un nombre o ID de contenedor.")
            return

        try:
            container = self.client.containers.get(nombre_o_id)

            estado = container.status
            print(f"Estado actual del contenedor '{nombre_o_id}': {estado}")

            if estado in ["exited", "created", "paused"]:
                container.start()
                print(f"Contenedor {container.id} iniciado.")
                time.sleep(2)
                container.reload()
                nuevo_estado = container.status
                print(f"Nuevo estado del contenedor '{nombre_o_id}': {nuevo_estado}")
                messagebox.showinfo("Éxito", f"El contenedor '{nombre_o_id}' ha sido iniciado. Estado actual: {nuevo_estado}.")
            else:
                messagebox.showinfo("Información", f"El contenedor '{nombre_o_id}' no está en un estado que permita iniciarse (estado actual: {estado}).")

        except NotFound:
            messagebox.showerror("Error", f"El contenedor con nombre o ID '{nombre_o_id}' no fue encontrado.")
        except APIError as e:
            messagebox.showerror("Error", f"Error al iniciar o obtener los logs del contenedor {nombre_o_id}: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")



    def eliminar_contenedor(self):
        nombre_o_id = simpledialog.askstring("Eliminar Contenedor", "Introduce el nombre o ID del contenedor que quieres borrar:")
        if not nombre_o_id:
                messagebox.showerror("Error", "No se proporcionó un nombre o ID de contenedor.")
                return

        try:
                container = self.client.containers.get(nombre_o_id)

                estado = container.status
                print(f"Estado actual del contenedor '{nombre_o_id}': {estado}")

                if estado == 'running':
                    confirmacion = messagebox.askyesno("Confirmación", f"El contenedor '{nombre_o_id}' está en ejecución. ¿Deseas detener y borrar este contenedor?")
                    if confirmacion:
                        print("Esta operación puede tardar unos segundos...")
                        container.stop(timeout=2)
                        print(f"Contenedor '{nombre_o_id}' detenido.")
                        container.remove(force=True)
                        print(f"Contenedor '{nombre_o_id}' ha sido eliminado.")
                        messagebox.showinfo("Éxito", f"Contenedor '{nombre_o_id}' detenido y eliminado.")
                    else:
                        print(f"Contenedor '{nombre_o_id}' no se ha eliminado.")
                        messagebox.showinfo("Información", f"Contenedor '{nombre_o_id}' no se ha eliminado.")
                else:
                    confirmacion = messagebox.askyesno("Confirmación", f"El contenedor '{nombre_o_id}' no está en ejecución (estado: {estado}). ¿Deseas eliminar este contenedor?")
                    if confirmacion:
                        print("Esta operación puede tardar unos segundos...")
                        container.remove(force=True)
                        print(f"Contenedor '{nombre_o_id}' ha sido eliminado.")
                        messagebox.showinfo("Éxito", f"Contenedor '{nombre_o_id}' ha sido eliminado.")
                    else:
                        print(f"Contenedor '{nombre_o_id}' no se ha eliminado.")
                        messagebox.showinfo("Información", f"Contenedor '{nombre_o_id}' no se ha eliminado.")

        except NotFound:
                messagebox.showerror("Error", f"No existe el contenedor con nombre o ID '{nombre_o_id}'.")
        except APIError as e:
                messagebox.showerror("Error", f"Error en la API de Docker: {str(e)}")


    def listar_imagenes(self):
            try:
                imagenes = self.client.images.list()

                if not imagenes:
                    print("No se encontraron imágenes.")
                    return

                for imagen in imagenes:
                    print(f"ID: {imagen.short_id}")
                    if imagen.tags:
                        for tag in imagen.tags:
                            print(f"  - Etiqueta: {tag}")
                    else:
                        print("  - Sin etiquetas")

            except APIError as e:
                print(f"Ha ocurrido un error con la API de Docker: {e}")

            except Exception as e:
                print(f"Ha ocurrido un error inesperado: {e}")

    def construir_imagen(self):
            nombre_o_id_contenedor = simpledialog.askstring("Construir Imagen", "Introduce el nombre o ID del contenedor:")
            if not nombre_o_id_contenedor:
                messagebox.showerror("Error", "No se proporcionó un nombre o ID de contenedor.")
                return

            nombre_imagen = simpledialog.askstring("Nombre de la Imagen", "Introduce el nombre de la nueva imagen (por ejemplo, 'mi_imagen'):")
            if not nombre_imagen:
                messagebox.showerror("Error", "No se proporcionó un nombre para la imagen.")
                return

            etiqueta_imagen = simpledialog.askstring("Etiqueta de la Imagen", "Introduce la etiqueta de la nueva imagen (por ejemplo, 'latest'):")
            if not etiqueta_imagen:
                messagebox.showerror("Error", "No se proporcionó una etiqueta para la imagen.")
                return

            try:
                contenedor = self.client.containers.get(nombre_o_id_contenedor)

                imagen = contenedor.commit(repository=nombre_imagen, tag=etiqueta_imagen)

                print(f"Imagen '{nombre_imagen}:{etiqueta_imagen}' creada a partir del contenedor '{nombre_o_id_contenedor}'.")
                print(f"ID de la nueva imagen: {imagen.id}")
                messagebox.showinfo("Éxito", f"Imagen '{nombre_imagen}:{etiqueta_imagen}' creada a partir del contenedor '{nombre_o_id_contenedor}'.")

            except NotFound:
                messagebox.showerror("Error", f"No existe el contenedor con nombre o ID '{nombre_o_id_contenedor}'.")
            except APIError as e:
                messagebox.showerror("Error", f"Error en la API de Docker: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {str(e)}")

    def eliminar_imagen(self):
            nombre_o_id_imagen = simpledialog.askstring("Eliminar Imagen", "Introduce el nombre o ID de la imagen que quieres borrar:")
            if not nombre_o_id_imagen:
                messagebox.showerror("Error", "No se proporcionó un nombre o ID de imagen.")
                return

            try:
                imagen = self.client.images.get(nombre_o_id_imagen)
                
                confirmacion = messagebox.askyesno("Confirmación", f"¿Estás seguro de que quieres eliminar la imagen '{nombre_o_id_imagen}'?")
                if confirmacion:
                    print("Esta operación puede tardar unos segundos...")
                    self.client.images.remove(imagen.id, force=True)
                    print(f"Imagen '{nombre_o_id_imagen}' ha sido eliminada.")
                    messagebox.showinfo("Éxito", f"Imagen '{nombre_o_id_imagen}' ha sido eliminada.")
                else:
                    print(f"Imagen '{nombre_o_id_imagen}' no se ha eliminado.")
                    messagebox.showinfo("Información", f"Imagen '{nombre_o_id_imagen}' no se ha eliminado.")

            except NotFound:
                messagebox.showerror("Error", f"No existe la imagen con nombre o ID '{nombre_o_id_imagen}'.")
            except APIError as e:
                messagebox.showerror("Error", f"Error en la API de Docker: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {str(e)}")
        
    def entrar_consola(self):
        nombre_contenedor = simpledialog.askstring("Nombre del Contenedor", "Ingrese el nombre del contenedor:")
        if not nombre_contenedor:
            print("No se proporcionó un nombre para el contenedor.")
            return

        try:
            contenedor = self.client.containers.get(nombre_contenedor)
            
            # Utiliza gnome-terminal para abrir una nueva ventana de terminal y ejecutar el comando de consola
            terminal_cmd = f"gnome-terminal -- bash -c 'docker exec -it {nombre_contenedor} /bin/bash; exec bash'"
            subprocess.run(terminal_cmd, shell=True)
            print(f"Consola abierta para el contenedor {nombre_contenedor}.")
        except APIError as e:
            print(f"Error al abrir la consola para el contenedor: {e}")
        except Exception as e:
            print(f"Otro error al intentar abrir la consola: {e}")


