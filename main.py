import email
import os
import zipfile
import json
import io

def procesar_email(archivo_eml):
    with open(archivo_eml, 'rb') as archivo:
        mensaje = email.message_from_bytes(archivo.read())
        remitente = mensaje['from']
        destinatario = mensaje['To']
        asunto = mensaje['Subject']
        fecha = mensaje['Date']
        cuerpo = ""
        if mensaje.is_multipart():
            for parte in mensaje.walk():
                tipo = parte.get_content_type()
                if tipo == "text/plain":
                    cuerpo += parte.get_payload(decode=True).decode()
        else:
            cuerpo = mensaje.get_payload(decode=True).decode()

        return remitente, destinatario,fecha, asunto, cuerpo

def recorrer_carpeta(carpeta):
  lista = []
  # Verifica que el directorio exista
  if os.path.exists(carpeta):
      # Recorre los archivos y subdirectorios dentro de la carpeta
      for nombre_archivo in os.listdir(carpeta):
          ruta = f'{carpeta}/{nombre_archivo}'
          # Ruta completa del archivo o subdirectorio
          ruta_completa = os.path.join(carpeta, nombre_archivo)
          lista.append(ruta)
  return lista

def to_json(lista):
    email = {
        "remitente": lista[0],
        "destinatario": lista[1],
        "fecha": lista[2],
        "asunto": lista[3],
        "cuerpo": lista[4]
    }
    return email

def main():
    archivos = recorrer_carpeta("./archivos")
    print(archivos)
    lista_emails = []
    for archivo in archivos:
        remitente, destinatario, fecha, asunto, cuerpo = procesar_email(archivo)
        lista_emails.append([remitente, destinatario, fecha, asunto, cuerpo])

    for i in range(len(lista_emails)):
        email = to_json(lista_emails[i])
        lista_emails[i] = email

    # Exportar la lista de diccionarios a un archivo JSON
    with open("salida.json", "w") as archivo_json:
        json.dump(lista_emails, archivo_json)

    print("Datos exportados correctamente a", "salida.json")
    #return lista_emails

