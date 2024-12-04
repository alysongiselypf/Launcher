import minecraft_launcher_lib
import os
import subprocess
import threading
import tkinter
import requests
from tkinter import PhotoImage, ttk, messagebox

# Configuración de la ventana principal
ventana = tkinter.Tk()
ventana.geometry('600x600')  # Tamaño de la ventana
ventana.title('Launcher Minecraft')  # Título de la aplicación
ventana.resizable(False, False)  # Tamaño fijo

# Fondo de pantalla
bg_image = PhotoImage(file="minecraft_background.png")  # Cambia este archivo por tu fondo de Minecraft
background_label = tkinter.Label(ventana, image=bg_image)
background_label.place(relwidth=1, relheight=1)

# Directorio de Minecraft
user_window = os.getlogin()
minecraft_directori = f"C:/Users/{user_window}/MinecraftLauncher"

# Estilo y tema
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), background="skyblue", padding=10)

# Widgets
label_nombre = tkinter.Label(ventana, text='Tu nombre', font=("Arial", 12), bg='white', fg='black')
label_nombre.place(x=50, y=50)

entry_nombre = tkinter.Entry(ventana, font=("Arial", 12))
entry_nombre.place(x=150, y=50, width=200)

label_ram = tkinter.Label(ventana, text='RAM a usar (en GB)', font=("Arial", 12), bg='white', fg='black')
label_ram.place(x=50, y=100)

entry_ram = tkinter.Entry(ventana, font=("Arial", 12))
entry_ram.place(x=200, y=100, width=150)

label_version = tkinter.Label(ventana, text="Versión de Minecraft", font=("Arial", 12), bg='white', fg='black')
label_version.place(x=50, y=150)

# Funciones principales con hilos
def run_async(func, *args):
    """Ejecutar una función en un hilo separado."""
    threading.Thread(target=func, args=args).start()

def listar_versiones_disponibles():
    """Obtener una lista de todas las versiones de Minecraft disponibles."""
    try:
        versiones = minecraft_launcher_lib.utils.get_version_list()
        versiones_disponibles = [version["id"] for version in versiones]
        return versiones_disponibles
    except Exception as e:
        print(f"Error al obtener las versiones disponibles: {e}")
        return []

def instalar_minecraft(version):
    """Instalar una versión de Minecraft."""
    try:
        if version:
            print(f"Iniciando instalación de Minecraft versión {version}...")
            minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directori)
            print(f"Instalación completada para la versión {version}")
            messagebox.showinfo("Éxito", f"Se instaló la versión {version}")
        else:
            print('No se ingresó ninguna versión')
    except Exception as e:
        print(f"Error durante la instalación de Minecraft: {e}")
        messagebox.showerror("Error", f"No se pudo instalar Minecraft: {e}")

def descargar_forge_installer(version):
    """Descargar el instalador de Forge para una versión específica de Minecraft."""
    try:
        # Ajustar el formato de la versión de Forge si es necesario
        forge_version = version.replace(".", "-")
        forge_url = f"https://files.minecraftforge.net/net/minecraftforge/forge/{version.replace('.', '/')}/forge-{version}-installer.jar"

        print(f"Intentando descargar Forge desde: {forge_url}")
        response = requests.get(forge_url, stream=True)
        if response.status_code != 200:
            raise Exception(f"No se encontró el instalador de Forge para la versión {version}.")

        # Guardar el instalador
        installer_path = os.path.join(minecraft_directori, f"forge-{version}-installer.jar")
        with open(installer_path, "wb") as installer_file:
            for chunk in response.iter_content(chunk_size=1024):
                installer_file.write(chunk)

        print(f"Instalador de Forge descargado correctamente en: {installer_path}")
        return installer_path
    except Exception as e:
        print(f"Error al descargar el instalador de Forge: {e}")
        messagebox.showerror("Error", f"No se pudo descargar el instalador de Forge: {e}")
        return None

def instalar_forge(version):
    """Instalar Forge utilizando el instalador descargado."""
    try:
        installer_path = descargar_forge_installer(version)
        if not installer_path:
            return

        print(f"Iniciando instalación de Forge desde {installer_path}...")
        subprocess.run(["java", "-jar", installer_path, "--installServer"], check=True)
        print("Forge instalado correctamente.")
        messagebox.showinfo("Éxito", "Forge se instaló correctamente.")
    except Exception as e:
        print(f"Error al instalar Forge: {e}")
        messagebox.showerror("Error", f"No se pudo instalar Forge: {e}")

def ejecutar_minecraft():
    """Ejecutar Minecraft con la configuración dada."""
    try:
        mine_user = entry_nombre.get()
        version = vers_instaladas.get()
        ram = f"-Xmx{entry_ram.get()}G"

        # Crear el perfil de Minecraft
        profile = minecraft_launcher_lib.profile.create_profile(version, minecraft_directori)

        # Configuración de la JVM y el usuario
        profile['minecraftArguments'] = f"--username {mine_user}"
        profile['jvmArguments'] = [ram]

        # Obtener el comando
        command = minecraft_launcher_lib.command.get_minecraft_command(profile)

        # Ejecutar Minecraft
        print(f"Iniciando Minecraft con la versión {version}...")
        subprocess.run(command)
    except Exception as e:
        print(f"Error al iniciar Minecraft: {e}")
        messagebox.showerror("Error", f"No se pudo iniciar Minecraft: {e}")

def actualizar_versiones_instaladas():
    """Actualizar el menú desplegable de versiones instaladas."""
    try:
        versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)
        versiones_instaladas_lista = [v['id'] for v in versiones_instaladas] if versiones_instaladas else ["Sin versiones instaladas"]
        vers_instaladas.set(versiones_instaladas_lista[0] if versiones_instaladas_lista else "Sin versiones instaladas")
        menu_instaladas['menu'].delete(0, 'end')
        for version in versiones_instaladas_lista:
            menu_instaladas['menu'].add_command(label=version, command=tkinter._setit(vers_instaladas, version))
    except Exception as e:
        print(f"Error al actualizar versiones instaladas: {e}")

# Obtener versiones disponibles e instaladas
versiones_disponibles = listar_versiones_disponibles()
versiones_instaladas_lista = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)
versiones_instaladas_lista = [v['id'] for v in versiones_instaladas_lista] if versiones_instaladas_lista else ["Sin versiones instaladas"]

# Menú desplegable para versiones disponibles
vers_disponibles = tkinter.StringVar(ventana)
vers_disponibles.set(versiones_disponibles[0] if versiones_disponibles else "Ninguna disponible")

versiones_menu_desplegable_disponibles = tkinter.OptionMenu(ventana, vers_disponibles, *versiones_disponibles)
versiones_menu_desplegable_disponibles.place(x=50, y=250)

# Menú desplegable para versiones instaladas
vers_instaladas = tkinter.StringVar(ventana)
vers_instaladas.set(versiones_instaladas_lista[0])

menu_instaladas = tkinter.OptionMenu(ventana, vers_instaladas, *versiones_instaladas_lista)
menu_instaladas.place(x=300, y=250)

# Botones
bt_instalar_version = ttk.Button(
    ventana,
    text="Instalar Versión",
    command=lambda: run_async(instalar_minecraft, vers_disponibles.get())
)
bt_instalar_version.place(x=50, y=350)

bt_instalar_forge = ttk.Button(
    ventana,
    text="Instalar Forge",
    command=lambda: run_async(instalar_forge, vers_instaladas.get())
)
bt_instalar_forge.place(x=50, y=450)

bt_actualizar_versiones = ttk.Button(
    ventana,
    text="Actualizar Lista",
    command=lambda: run_async(actualizar_versiones_instaladas)
)
bt_actualizar_versiones.place(x=200, y=400)

bt_ejecutar_minecraft = ttk.Button(
    ventana,
    text="Iniciar Minecraft",
    command=lambda: run_async(ejecutar_minecraft)
)
bt_ejecutar_minecraft.place(x=300, y=450)

# Mostrar la ventana
ventana.mainloop()

