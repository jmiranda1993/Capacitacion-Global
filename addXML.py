import xml.etree.ElementTree as ET
import sys
import os
import json
from utilidades import read_config
import argparse


NAMESPACE = "http://soap.sforce.com/2006/04/metadata"
ET.register_namespace('', NAMESPACE)  # Registrar el namespace

def create_global_xml(path):
    root = ET.Element(f"{{{NAMESPACE}}}Package")
    version = ET.SubElement(root, f"{{{NAMESPACE}}}version")
    version.text = "63.0"
    tree = ET.ElementTree(root)
    with open(path, "wb") as f:
        tree.write(f, encoding='UTF-8', xml_declaration=True)

def indent(elem, level=0):
    """Ajusta el formato para que el XML tenga sangrías."""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def fusionar_nodos_duplicados(global_root):
    """Fusionar nodos <types> duplicados en el XML global."""
    unique_types = {}
    for g_type in global_root.findall(f"{{{NAMESPACE}}}types"):
        type_name = g_type.find(f"{{{NAMESPACE}}}name").text
        if type_name in unique_types:
            # Fusionar miembros
            existing_type = unique_types[type_name]
            existing_members = {member.text for member in existing_type.findall(f"{{{NAMESPACE}}}members")}
            for member in g_type.findall(f"{{{NAMESPACE}}}members"):
                if member.text not in existing_members:
                    existing_type.append(member)
            global_root.remove(g_type)
        else:
            unique_types[type_name] = g_type

def ordenar_miembros(global_root):
    """Sort the <members> nodes alphabetically (case insensitive) within each <types>."""
    for g_type in global_root.findall(f"{{{NAMESPACE}}}types"):
        members_nodes = g_type.findall(f"{{{NAMESPACE}}}members")
        members_nodes_sorted = sorted(members_nodes, key=lambda x: x.text.lower())  # Uso de lower() para ordenamiento Case Insensitive
        for m in members_nodes:
            g_type.remove(m)
        for m in members_nodes_sorted:
            g_type.append(m)

def ordenar_tipos_por_nombre(global_root):
    """Ordenar los nodos <types> alfabéticamente según el nodo <name>."""
    types_nodes = list(global_root.findall(f"{{{NAMESPACE}}}types"))
    for t in types_nodes:
        global_root.remove(t)
    types_nodes.sort(key=lambda x: x.find(f"{{{NAMESPACE}}}name").text)
    for t in types_nodes:
        global_root.append(t)

def combinar_xml(global_path, parcial_path, output_path):
    # Verificar si global.xml existe. Si no existe, crearlo.
    if not os.path.exists(global_path):
        create_global_xml(global_path)
    global_tree = ET.parse(global_path)
    global_root = global_tree.getroot()

    parcial_tree = ET.parse(parcial_path)
    parcial_root = parcial_tree.getroot()

    for p_type in parcial_root.findall(f"{{{NAMESPACE}}}types"):
        p_name_node = p_type.find(f"{{{NAMESPACE}}}name")
        p_name = p_name_node.text
        
        # Buscar en el XML global si ya existe este tipo
        g_type = global_root.find(f"{{{NAMESPACE}}}types[{{{NAMESPACE}}}name='{p_name}']")
        
        # Si el tipo ya existe, agregar los miembros
        if g_type is not None:
            g_members = {mem.text for mem in g_type.findall(f"{{{NAMESPACE}}}members")}
            for p_member in p_type.findall(f"{{{NAMESPACE}}}members"):
                if p_member.text not in g_members:
                    g_type.append(p_member)
        # Si el tipo no existe, agregar todo el nodo al XML global
        else:
            global_root.append(p_type)

    # Fusionar nodos <types> duplicados
    fusionar_nodos_duplicados(global_root)

    # Ordenar los nodos <members> alfabéticamente dentro de cada <types>
    ordenar_miembros(global_root)

    # Asegurarse de que el nodo <name> sea el último en cada nodo <types>
    for g_type in global_root.findall(f"{{{NAMESPACE}}}types"):
        name_node = g_type.find(f"{{{NAMESPACE}}}name")
        if name_node is not None:
            g_type.remove(name_node)
            g_type.append(name_node)

    # Mover el nodo <version> al final
    version_node = global_root.find(f"{{{NAMESPACE}}}version")
    if version_node is not None:
        global_root.remove(version_node)

    # Ordenar los nodos <types> alfabéticamente según el nodo <name>
    ordenar_tipos_por_nombre(global_root)

    # Agregar nuevamente el nodo <version> al final
    if version_node is not None:
        global_root.append(version_node)

    # Ajusta el formato del XML
    indent(global_root)

    # Escribir el archivo XML con finales de línea \n
    with open(output_path, 'wb') as f:
        global_tree.write(f, encoding='UTF-8', xml_declaration=True)    # unicode
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesar archivos XML.")
    
    # Argumento para el archivo XML parcial con sus alias
    parser.add_argument('--xmlPartial', '-xp', required=True, help="Nombre del archivo XML parcial.")
    
    # Argumento opcional para el archivo XML global con sus alias
    parser.add_argument('--xmlGlobal', '-xg', help="Nombre opcional del archivo XML global.")

    args = parser.parse_args()

    # Si se proporciona el argumento xmlGlobal, usar ese como el nombre del archivo global
    if args.xmlGlobal is not None:
        global_filename = args.xmlGlobal
    else:
        # De lo contrario, leer el nombre del archivo global desde la configuración
        config = read_config()
        global_filename = config.get('GlobalXML', 'global.xml')

    # Si el valor es un string vacío o None, usar el valor por defecto 'global.xml'
    if not global_filename:
        global_filename = 'global.xml'

    # Al combinar los archivos, el archivo de salida será el mismo que el archivo global especificado
    combinar_xml(global_filename, args.xmlPartial, global_filename)
    
    # Mensaje final para informar al usuario
    print(f"Archivo global generado: {global_filename}")
