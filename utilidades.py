import json

def read_config(filename='certa.json'):
    """Lee el archivo de configuración y devuelve un diccionario con la configuración."""
    with open(filename, 'r') as f:
        config = json.load(f)
    return config
