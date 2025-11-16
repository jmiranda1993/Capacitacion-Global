import sys
import subprocess
import shutil
from tabulate import tabulate
from colorama import Fore, Style
import os
import platform



def ejecutar_comando(sfalias, archivo):
    comando = f"vlocity --sfdx.username {sfalias} --job manifest/{archivo} packGetDiffs > onlychanged.txt"
    subprocess.run(comando, shell=True)

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        print(f"+ Lista de Diferencias")
        contadorelementos = 0
        resultados = []
        for linea in lineas:
            elementos = linea.split(' ')
            in_org = ' '
            in_branch = ' '
            try:
                estado = elementos[5]
                if 'Changed' in estado or 'New' in estado:
                    contadorelementos = contadorelementos + 1
                    contenido = linea.split('>>')[1].strip()
                    contenidotabla = contenido.split(' ')
                    resultadotabla = contenidotabla[1]
                    if 'Changed' in estado:
                        in_org = f'{Fore.YELLOW}✓{Style.RESET_ALL}'
                        in_branch = f'{Fore.GREEN}✓{Style.RESET_ALL}'
                    if 'New' in estado and os.path.exists('Vlocity/'+resultadotabla):
                        in_org = "Faltante"
                        in_branch = f'{Fore.GREEN}✓{Style.RESET_ALL}'
                    if 'New' in estado and not os.path.exists('Vlocity/'+resultadotabla):
                        in_org = "Sobrante"
                        in_branch = f'❌'
                    resultados.append([contadorelementos, estado, resultadotabla, in_branch, in_org])
            except IndexError:
                # Si la línea no tiene al menos 6 elementos, se omite
                pass
        tabla = tabulate(resultados, headers=[Fore.GREEN + "#", Fore.GREEN + "Estado", "Componentes", "En Branch", "En Org"], tablefmt="fancy_grid")
        tabla = tabla.replace(Fore.GREEN, Style.RESET_ALL + Fore.GREEN) # Restablece el color después de los encabezados
        print(tabla)
        print(f"Diferencias Encontradas: " + str(contadorelementos))
    # eliminar_changed = f"rm onlychanged.txt"
    # subprocess.run(eliminar_changed, shell=True)
    shutil.os.unlink(nombre_archivo)
    restaura_rama = f"git reset --hard"
    subprocess.run(restaura_rama, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Finalizado.")

def ejecutar_checkout(ext, os_system):
    comando_checkout = f"manifest.{ext}"
    if os_system == 'Linux':
        comando = f"chmod +x {comando_checkout}"
        subprocess.run(comando, shell=True)
        execcheckout = f'./{comando_checkout}'
        subprocess.run(execcheckout, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif os_system == 'Windows':
        subprocess.run(comando_checkout, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Estructura de Directorio Actualizada.")
    shutil.os.unlink(comando_checkout)
    print("Se completa proceso Shell.")
    print("Espere mientras se crea la lista.")

def eliminar_directorio(ruta_directorio):
    try:
        shutil.rmtree(ruta_directorio)
        print(f"Componentes {ruta_directorio} Seleccionados exitosamente.")
    except OSError as e:
        print(f"No se pudo eliminar el directorio {ruta_directorio}. Error: {e}")

def procesar_archivo(archivo,ext):
    with open(f"manifest/{archivo}", "r") as file:
        contenido = file.readlines()
    manifest_valores = []
    capturar = False
    for linea in contenido:
        if linea.strip() == "manifest:":
            capturar = True
        elif capturar and "-" in linea:
            manifest_valores.append(linea.strip())
    scrpitName = f"manifest.{ext}"
    print("scrpitName: " + scrpitName)
    with open(scrpitName, "w") as manifest_file:
        for valor in manifest_valores:
            nombre_archivo = valor.replace("-", "").strip()
            manifest_file.write(f"git checkout Vlocity/{nombre_archivo}\n")

def main():
    # Capturar los argumentos de línea de comandos
    os_system = platform.system()
    if os_system == 'Linux':
        print('SO: Linux')
        ext='sh'
    elif os_system == 'Windows':
        print('SO: Windows')
        ext='bat'

    sfalias = sys.argv[1]
    print("Alias: " + sfalias)
    archivo = sys.argv[2]
    print("Archivo: " + archivo)

    procesar_archivo(archivo,ext)
    print("Shell procesado con éxito.")
    eliminar_directorio('Vlocity')
    ejecutar_checkout(ext,os_system)
    ejecutar_comando(sfalias, archivo)
    leer_archivo('onlychanged.txt')

if __name__ == "__main__":
    main()