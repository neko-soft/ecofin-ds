# Importar librerías

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from datetime import date
import pytz


# Leer datos con las URLs
url = pd.read_csv('urls.csv')
url = url['urls'].tolist()


# Realizamos la solicitud HTTP para obtener el contenido de la página
response = requests.get(url[1])

# Verificamos si la solicitud fue exitosa (código 200)
if response.status_code == 200:
    # Analizamos el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')



    data = []

    # Para saber cómo sacar los datos, hay que hacer un Inspect Element en la página
    # Desde ahí, buscar el class=ABC, y ajustar si es necesario.
    # Mientras no cambien la página no debería haber problema.
    for td in soup.find_all("td", class_="datatable_cell__LJp3C"):
        precio = td.text.strip()
        data.append(precio)



    # Crear una lista de tuplas de 3 elementos: fecha, precio, variación
    chunks = [(data[i], data[i+1], data[i+2]) for i in range(0, len(data), 3)]

    # Convertirlo a un DataFrame
    df = pd.DataFrame(chunks, columns=['Fecha', 'Precio', 'Variación'])

    # Convertir la columna 'Fecha' a tipo datetime
    # Porque de verdad que es asqueroso el formato que usan los gringos
    # ¿¡Qué es esa aberración de poner Mes - Día - Año!?
    # O sea, va de mayor a menor a más mayor... que imbecilidad más grande
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%b %d, %Y')
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')

    # Convertir la columna 'Precio' a número flotante
    df['Precio'] = pd.to_numeric(df['Precio'].str.replace(',', ''), errors='coerce')

    # Convertir la columna 'Variación' a número flotante, eliminando el símbolo '%' y convirtiéndolo a tipo numérico
    df['Variación'] = df['Variación'].str.replace('%', '').astype(float)

    # Ordenar de fecha más antigua a más reciente.
    df = df.sort_values(by='Fecha', ascending=True)
    print (df)





    ipsaCompleto = pd.read_csv('datos/ipsaCompleto.csv')
    ipsaCompleto['Fecha'] = pd.to_datetime(ipsaCompleto['Fecha'], format='%Y-%m-%d')
    # Verificar cómo quedaron las fechas
    print(ipsaCompleto)





    # Obtener la hora de Santiago de Chile para verificar después
    # si la bolsa aún está abierta o no.
    horaActual = datetime.now(pytz.timezone("America/Santiago")).time()
    print (horaActual)

    # Iterar sobre las fechas de los nuevos datos y buscar si existen en los históricos
    for _, row in df.iterrows():
        # Buscar si la fecha del nuevo DataFrame existe en el histórico
        historical_row = ipsaCompleto.loc[ipsaCompleto['Fecha'] == row['Fecha']]


        if not historical_row.empty:
            # Si encontramos la fecha, comparar los precios
            historical_price = historical_row['Valor IPSA'].values[0]
            if historical_price != row['Precio']:
                print(f"¡Precio diferente en {row['Fecha']}! Nuevo: {row['Valor IPSA']} - Histórico: {historical_price}")
            else:
                print (f"Los precios en {row['Fecha']} están bien :D. Precio: {row['Precio']}")
        
        # Este elif verifica la fecha de hoy con las fechas de los rows, si está la misma fecha de hoy en los datos
        # verifica si la hora es antes de las 16:30 de Santiago de Chile. Si es así, entonces no actualiza el dato
        # porque la bolsa aún está abierta, y el precio final puede variar.
        elif row['Fecha'].date() == date.today() and horaActual <= datetime.strptime("16:30:00", "%H:%M:%S").time():
            print (f"No se agregará el dato de la fecha {row['Fecha']} porque la bolsa aún está abierta")
        else: 
            print(f"¡Fecha {row['Fecha']} no encontrada en los datos históricos! Precio: {row['Precio']}")
            # Agregar nuevos datos si es que hay.
            new_row = pd.DataFrame({'Fecha': [row['Fecha']], 'Valor IPSA': [row['Precio']]})
            ipsaCompleto = pd.concat([ipsaCompleto, new_row], ignore_index=True)
            print (f"Se ha agregado la fecha {row['Fecha']} con el siguiente precio: {row['Precio']}")

    ipsaCompleto.to_csv("datos/ipsaCompleto.csv", index=False)



else:
    print(f"Error al obtener la página, código de estado: {response.status_code}")




