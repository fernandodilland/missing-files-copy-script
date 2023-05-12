import os
import shutil
import time
from tkinter import Tk
from tkinter.filedialog import askdirectory

def obtener_archivos_faltantes(origen, destino):
    archivos_faltantes = []
    for root, dirs, files in os.walk(origen):
        subdirectorio = os.path.relpath(root, origen)
        destino_actual = os.path.join(destino, subdirectorio)
        for file in files:
            origen_archivo = os.path.join(root, file)
            destino_archivo = os.path.join(destino_actual, file)
            if not os.path.exists(destino_archivo):
                archivos_faltantes.append(origen_archivo)
    return archivos_faltantes

def copiar_archivos(origen, destino):
    if not os.path.exists(destino):
        os.makedirs(destino)

    archivos_faltantes = obtener_archivos_faltantes(origen, destino)

    if len(archivos_faltantes) == 0:
        print("El destino ya cuenta con todos los archivos. No se realizará la copia.")
        return

    total_archivos = 0
    tiempo_inicial = time.time()
    errores = []

    for archivo in archivos_faltantes:
        try:
            destino_archivo = archivo.replace(origen, destino)
            if os.path.isdir(archivo):
                shutil.copytree(archivo, destino_archivo)
            else:
                shutil.copy2(archivo, destino_archivo)
            total_archivos += 1
            time.sleep(1)
        except Exception as e:
            errores.append(str(e))

    tiempo_transcurrido = time.time() - tiempo_inicial

    registro_archivo = "registro.txt"
    if os.path.exists(registro_archivo):
        os.remove(registro_archivo)

    with open(registro_archivo, "w") as file:
        file.write("Cantidad de archivos: {}\n".format(total_archivos))
        file.write("Tiempo transcurrido: {:.2f} segundos\n".format(tiempo_transcurrido))
        if errores:
            file.write("\nErrores:\n")
            for error in errores:
                file.write("- {}\n".format(error))

    print("¡La copia de archivos se ha completado!")

Tk().withdraw()
origen_dir = askdirectory(title="Seleccionar directorio de origen")

Tk().withdraw()
destino_dir = askdirectory(title="Seleccionar directorio de destino")

try:
    copiar_archivos(origen_dir, destino_dir)
except Exception as e:
    print("Error durante la copia de archivos:", str(e))
