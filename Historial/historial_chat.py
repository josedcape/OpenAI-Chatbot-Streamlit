import json
import os
import time  # Para obtener la fecha y hora

def cargar_historial():
    ruta_historial = os.path.join("Historial", "chat_history.json")
    try:
        with open(ruta_historial, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open(ruta_historial, "w") as f:  # Crea el archivo si no existe
            json.dump([], f)
        return []
    except json.JSONDecodeError:  # Maneja el error de decodificación
        st.warning("El historial de chat está dañado o vacío. Se creará un nuevo historial.")
        with open(ruta_historial, "w") as f:
            json.dump([], f)
        return []

def guardar_historial(historial, max_mensajes=100):  # Limitar el historial a 100 mensajes
    ruta_historial = os.path.join("historial", "chat_history.json")
    try:
        # Limitar el historial
        historial = historial[-max_mensajes:]

        # Agregar marcas de tiempo
        for mensaje in historial:
            if "timestamp" not in mensaje:
                mensaje["timestamp"] = time.time()

        with open(ruta_historial, "w") as f:
            json.dump(historial, f, indent=4)
    except Exception as e:  # Atrapar cualquier excepción al guardar
        print(f"Error al guardar el historial: {e}")
