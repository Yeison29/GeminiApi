import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.steren.com.co/videovigilancia-y-seguridad/camaras-cctv'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Buscar elementos HTML que contengan la información de las cámaras (por ejemplo, nombres, precios, etc.)
camaras = soup.find_all('li', class_='product-item')

# Extraer los datos y guardarlos en una lista
datos_camaras = []

for camara in camaras:
    # Intentar obtener el título
    titulo_tag = camara.find('h2')
    titulo = titulo_tag.text if titulo_tag else 'No disponible'

    # Intentar obtener el precio
    precio_tag = camara.find('span', class_='price')
    precio = precio_tag.text if precio_tag else 'No disponible'
    precio = precio.replace('$', '')

    imagen_tag = camara.find('img')
    src_imagen = imagen_tag.get('src') if imagen_tag else 'No disponible'

    # Guardar la información en la lista
    datos_camaras.append({'Titulo': titulo, 'Precio': precio, 'Imagen': src_imagen})

# Guardar los datos en un archivo CSV
with open('camaras.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Titulo', 'Precio', 'Imagen']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(datos_camaras)

print(f"Se han guardado {len(datos_camaras)} productos en el archivo 'camaras.csv'.")
