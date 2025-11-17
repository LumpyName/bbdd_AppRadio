import sys
import os
import json

def drive_to_raw(url: str) -> str:
    """
    Convierte un enlace normal de Google Drive en un enlace RAW (descarga directa).
    Si el enlace no pertenece a Drive, retorna un mensaje de error.
    """

    if "drive.google.com" not in url:
        return " El enlace no es de Google Drive."

    # Extraer ID del archivo
    try:
        # Ejemplos:
        # https://drive.google.com/file/d/ID/view?usp=sharing
        # https://drive.google.com/open?id=ID
        # https://drive.google.com/uc?id=ID&export=download

        if "/file/d/" in url:
            file_id = url.split("/file/d/")[1].split("/")[0]
        elif "id=" in url:
            file_id = url.split("id=")[1].split("&")[0]
        else:
            return " No se pudo extraer el ID del enlace."

    except Exception:
        return " Error procesando el enlace."

    # Construir enlace RAW
    raw_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    return raw_url


def leer_json(archivo="contenidos.json"):
    """
    Lee y retorna todo el contenido del archivo JSON como una lista de diccionarios.
    Si no existe o está vacío/corrupto, retorna una lista vacía.
    """
    if not os.path.exists(archivo):
        return []

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []  # Si el JSON no es una lista, lo tratamos como vacío
    except (json.JSONDecodeError, ValueError):
        return []  # Si está corrupto o vacío


def guardar_en_json(contenido, archivo="contenidos.json"):
    """
    Guarda el contenido en un archivo JSON.
    Si el archivo no existe, lo crea.
    Si existe, lee la lista actual y agrega el nuevo elemento.
    """

    # Si el archivo no existe, crear una lista vacía
    if not os.path.exists(archivo):
        datos = []
    else:
        # Si existe, leer su contenido
        with open(archivo, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
                if not isinstance(datos, list):
                    datos = []  # Si el JSON no es lista, lo re-inicializamos
            except json.JSONDecodeError:
                datos = []  # Si está corrupto o vacío, iniciar lista

    # Agregar el nuevo contenido
    datos.append(contenido)

    # Guardar todo de nuevo
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    print(f"\n Guardado correctamente en {archivo}")

USO = """
Uso correcto:
    python crear_contenido.py "TÍTULO" "DESCRIPCIÓN" "THUMBNAIL_URL" "AUDIO_URL"

Ejemplo:
    python crear_contenido.py "Canción épica" "El mejor tema" \\
    "https://dominio.com/thumb.jpg" \\
    "https://dominio.com/audio.mp3"
"""

def main():
    # Se esperan exactamente 4 argumentos (más el nombre del script)
    if len(sys.argv) != 5:
        print(" ERROR: Parámetros incompletos.\n")
        print(USO)
        return
    
    _, titulo, descripcion, thumbnail_url, audio_url = sys.argv

    print(" Datos recibidos correctamente:")
    print(f"  - Título: {titulo}")
    print(f"  - Descripción: {descripcion}")
    print(f"  - Thumbnail URL: {thumbnail_url}")
    print(f"  - Audio URL: {audio_url}")

    # Aquí NO hacemos nada todavía, solo preparamos la estructura
    contenido = {
        "titulo": titulo,
        "descripcion": descripcion,
        "thumbnail_url": thumbnail_url,
        "audio_url": drive_to_raw(audio_url)
    }

    guardar_en_json(contenido)

if __name__ == "__main__":
    main()

