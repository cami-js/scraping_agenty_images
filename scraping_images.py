import os  
import requests  
from bs4 import BeautifulSoup  
from urllib.parse import urljoin  

#Función para crear la carpeta si no existe
def crear_carpeta(carpeta):
    if not os.path.exists(carpeta):  
        os.makedirs(carpeta)  

#Función para descargar la imagen
def descargar_imagen(url, carpeta):
    try:
        response = requests.get(url, stream=True)  
        response.raise_for_status()  

        nombre_imagen = url.split("/")[-1]

        ruta_imagen = os.path.join(carpeta, nombre_imagen)

        #Guardar la imagen en el archivo
        with open(ruta_imagen, 'wb') as f:
            for chunk in response.iter_content(1024):  #Descargar en trozos de 1024 bytes
                f.write(chunk)
        print(f"Imagen descargada: {nombre_imagen}")
    except requests.exceptions.RequestException as e:
        print(f"No se pudo descargar la imagen {url}. Error: {e}")

#Función para verificar si la imagen tiene el formato deseado
def es_formato_valido(src):
    formatos_validos = (".png", ".jpg", ".webp")  
    return src.lower().endswith(formatos_validos)  

#Función principal del web scraper
def scrape_imagenes(url, carpeta):
    crear_carpeta(carpeta)  
    
    try:
        response = requests.get(url)  
        response.raise_for_status()  
        
        soup = BeautifulSoup(response.content, 'html.parser')  
        
        for img_tag in soup.find_all('img'): 
            src = img_tag.get('src')  
            if src and es_formato_valido(src):  
                imagen_url = urljoin(url, src)  
                descargar_imagen(imagen_url, carpeta)  
    except requests.exceptions.RequestException as e:
        print(f"No se pudo acceder a la página {url}. Error: {e}")

url = "https://agenty.com/"

carpeta = "imagenes"

scrape_imagenes(url, carpeta)
