import minecraft_launcher_lib
import os
import subprocess
import tkinter
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
user_window = os.environ["USERNAME"]
minecraft_directori = f"C:/Users/{user_window}/AppData/Roaming/.minecraftLauncher"

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

# Funciones principales
def instalar_minecraft(version):
    """Instalar una versión de Minecraft."""
    if version:
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directori)
        print(f'Se ha instalado la versión {version}')
    else:
        print('No se ingresó ninguna versión')

def instalar_forge(version):
    """Instalar Forge para una versión específica."""
    try:
        forge_versions = ['1.16.5-36.2.39', '1.12.2-14.23.5.2854', '1.18.2-40.1.0', '1.19.2-40.2.5']
        forge_disponibles = [f"Forge para {version}" for version in forge_versions]
        
        if forge_disponibles:
            print(f'{forge_disponibles[0]} instalado para la versión {version}')
        else:
            print(f'No se encontró Forge para la versión {version}')
    except Exception as e:
        print(f"Error al instalar Forge: {e}")

def instalar_mods(version_minecraft):
    """Instalar mods para una versión específica de Minecraft."""
    mods_path = f"{minecraft_directori}/mods"
    if not os.path.exists(mods_path):
        os.makedirs(mods_path)
    
    mods = ["mod1.jar", "mod2.jar"]
    for mod in mods:
        subprocess.run(["cp", mod, mods_path])  # Copiar el mod a la carpeta de mods
        print(f"Mod {mod} instalado.")

def listar_versiones_minecraft_ui():
    """Crear una ventana para mostrar las versiones de Minecraft disponibles."""
    ventana_versiones = tkinter.Toplevel(ventana)
    ventana_versiones.geometry("300x200")
    ventana_versiones.title("Seleccionar Versión Minecraft")

    label_version = tkinter.Label(ventana_versiones, text="Selecciona la versión de Minecraft", font=("Arial", 12))
    label_version.pack(pady=10)

    versiones_minecraft = minecraft_launcher_lib.utils.get_version_list()[:5]  # Tomamos solo las 5 primeras
    versiones_disponibles = [v['id'] for v in versiones_minecraft]

    version_var = tkinter.StringVar(ventana_versiones)
    version_var.set(versiones_disponibles[0])

    versiones_menu = tkinter.OptionMenu(ventana_versiones, version_var, *versiones_disponibles)
    versiones_menu.pack(pady=10)

    bt_instalar = tkinter.Button(ventana_versiones, text="Instalar", font=("Arial", 12),
                                 command=lambda: instalar_minecraft(version_var.get()))
    bt_instalar.pack(pady=10)

def listar_versiones_forge_ui():
    """Crear una ventana para mostrar las versiones de Forge disponibles."""
    ventana_forge = tkinter.Toplevel(ventana)
    ventana_forge.geometry("300x200")
    ventana_forge.title("Seleccionar Forge")

    version_minecraft = vers.get()

    forge_versions = ['1.16.5-36.2.39', '1.12.2-14.23.5.2854', '1.18.2-40.1.0', '1.19.2-40.2.5']
    forge_disponibles = [f"Forge para {version}" for version in forge_versions]

    if not forge_disponibles:
        forge_disponibles = ["No hay versiones de Forge disponibles"]

    forge_var = tkinter.StringVar(ventana_forge)
    forge_var.set(forge_disponibles[0])

    forge_menu = tkinter.OptionMenu(ventana_forge, forge_var, *forge_disponibles)
    forge_menu.pack(pady=10)

    bt_instalar_forge = tkinter.Button(ventana_forge, text="Instalar Forge", font=("Arial", 12),
                                       command=lambda: instalar_forge(forge_var.get()))
    bt_instalar_forge.pack(pady=10)

def ejecutar_minecraft():
    """Ejecutar Minecraft con la configuración dada."""
    mine_user = entry_nombre.get()
    version = vers.get()
    ram = f"-Xmx{entry_ram.get()}G"

    options = {
        'username': mine_user,
        'jvmArguments': [ram],
        'launcherName': "Custom Launcher",
    }

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directori, options)
    subprocess.run(minecraft_command)

def comprobar_actualizaciones():
    """Comprobar si hay actualizaciones disponibles para Minecraft."""
    versiones_disponibles = minecraft_launcher_lib.utils.get_version_list()
    version_instalada = vers.get()
    if version_instalada != versiones_disponibles[0]['id']:
        respuesta = messagebox.askyesno("Actualización disponible", "¿Quieres actualizar Minecraft?")
        if respuesta:
            instalar_minecraft(versiones_disponibles[0]['id'])

# Función auxiliar para crear ventanas secundarias
def ventana_instalar_version(callback):
    ventana_versiones = tkinter.Toplevel(ventana)
    ventana_versiones.geometry("300x200")
    ventana_versiones.title("Instalar Versión")

    label_version = tkinter.Label(ventana_versiones, text="Versión:", font=("Arial", 12))
    label_version.pack(pady=10)

    entry_version = tkinter.Entry(ventana_versiones, font=("Arial", 12))
    entry_version.pack(pady=10)

    bt_instalar = tkinter.Button(ventana_versiones, text="Instalar", font=("Arial", 12),
                                 command=lambda: callback(entry_version.get()))
    bt_instalar.pack(pady=10)

# Menú desplegable para versiones instaladas
versiones_instaladas_lista = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)
versiones_instaladas_lista = [v['id'] for v in versiones_instaladas_lista] if versiones_instaladas_lista else ["Sin versiones instaladas"]

vers = tkinter.StringVar(ventana)
vers.set(versiones_instaladas_lista[0])

versiones_menu_desplegable = tkinter.OptionMenu(ventana, vers, *versiones_instaladas_lista)
versiones_menu_desplegable.place(x=50, y=200)

# Botones
bt_instalar_minecraft = ttk.Button(ventana, text='Instalar Minecraft', command=listar_versiones_minecraft_ui)
bt_instalar_minecraft.place(x=50, y=300)

bt_instalar_forge = ttk.Button(ventana, text='Instalar Forge', command=listar_versiones_forge_ui)
bt_instalar_forge.place(x=200, y=300)

bt_instalar_mods = ttk.Button(ventana, text='Instalar Mods', command=lambda: instalar_mods(vers.get()))
bt_instalar_mods.place(x=350, y=300)

bt_ejecutar_minecraft = ttk.Button(ventana, text="Iniciar", command=ejecutar_minecraft, style="TButton")
bt_ejecutar_minecraft.place(x=500, y=550, anchor="se")

# Comprobar actualizaciones
ventana.after(1000, comprobar_actualizaciones)

# Mostrar la ventana principal
ventana.mainloop()
