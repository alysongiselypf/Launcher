import minecraft_launcher_lib
import os
import subprocess
import tkinter
from tkinter import PhotoImage

# Configurar la ventana principal
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

# Widgets
label_nombre = tkinter.Label(ventana, text='Tu nombre', font=("Arial", 12), bg='white', fg='black')
label_nombre.place(x=50, y=50)

entry_nombre = tkinter.Entry(ventana, font=("Arial", 12))
entry_nombre.place(x=150, y=50, width=200)

label_ram = tkinter.Label(ventana, text='RAM a usar (en GB)', font=("Arial", 12), bg='white', fg='black')
label_ram.place(x=50, y=100)

entry_ram = tkinter.Entry(ventana, font=("Arial", 12))
entry_ram.place(x=200, y=100, width=150)

# Botón para iniciar Minecraft
bt_ejecutar_minecraft = tkinter.Button(ventana, text="Iniciar", bg='green', fg='white', font=("Arial", 12),
                                        command=lambda: ejecutar_minecraft(entry_nombre.get(), vers))
bt_ejecutar_minecraft.place(x=500, y=550, anchor="se")

# Variable global para almacenar la entrada de versiones
entry_versiones = None

def instalar_minecraft():
    global entry_versiones
    if entry_versiones:  # Verificar que entry_versiones esté definido
        version = entry_versiones.get()
        if version:
            minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directori)
            print(f'Se ha instalado la versión {version}')
        else:
            print('No se ingresó ninguna versión')
    else:
        print('No se ha inicializado el campo de versiones')

def instalar_versiones_normales():
    global entry_versiones
    ventana_versiones = tkinter.Toplevel(ventana)
    entry_versiones = tkinter.Entry(ventana_versiones)
    entry_versiones.place(x=0, y=0)  # Posición del Entry

    bt_instalar_vers = tkinter.Button(
        ventana_versiones, command=instalar_minecraft, text='Instalar')
    bt_instalar_vers.place(x=0, y=50)  # Posición del botón


# Función para instalar Minecraft
def instalar_minecraft():
    version = entry_versiones.get()
    if version:
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directori)
        print(f'Se ha instalado la versión {version}')
    else:
        print('No se ingresó ninguna versión')

# Función para instalar Forge
def instalar_forge():
    version = entry_versiones.get()
    forge = minecraft_launcher_lib.forge.find_forge_version(version)
    minecraft_launcher_lib.forge.install_forge_version(forge, minecraft_directori)
    print('Forge instalado')

# Función para ejecutar Minecraft
def ejecutar_minecraft(nombre, vers):
    version = vers.get()
    ram = f"-Xmx{entry_ram.get()}G"
    options = {
        'username': nombre,
        'jvmArguments': [ram],
        'launcherName': "Custom Launcher",
    }
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directori, options)
    subprocess.run(minecraft_command)

# Menú desplegable para versiones instaladas
versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)
versiones_instaladas_lista = [v['id'] for v in versiones_instaladas] if versiones_instaladas else ["Sin versiones instaladas"]

vers = tkinter.StringVar(ventana)
vers.set(versiones_instaladas_lista[0])

versiones_menu_desplegable = tkinter.OptionMenu(ventana, vers, *versiones_instaladas_lista)
versiones_menu_desplegable.place(x=50, y=200)

# Botones para instalar versiones
bt_instalar_versiones = tkinter.Button(ventana, text='Instalar versiones', bg='skyblue', font=("Arial", 12),
                                        command=lambda: instalar_minecraft())
bt_instalar_versiones.place(x=50, y=300)

bt_instalar_forge = tkinter.Button(ventana, text='Instalar Forge', bg='skyblue', font=("Arial", 12),
                                    command=lambda: instalar_forge())
bt_instalar_forge.place(x=200, y=300)

# Mostrar la ventana
ventana.mainloop()
