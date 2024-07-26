import matplotlib.pyplot as plt
import numpy as np


# La función leer_txt() se encarga de abrir el archivo, guardar su contenido y volver a cerrarlo.
# Devuelve cada línea como un string dentro de una lista.
def leer_txt(nombre_archivo) :
    archivo = open(nombre_archivo, 'r' )
    lineas = archivo.readlines()
    archivo.close()
    return lineas


# La función limpiar_datos() recibe una lista y se encarga de eliminar caracteres como \n y de separar cada palabra.
# De esta forma los datos quedarán separados y formateados para su posterior análisis.
# Devuelve una lista, que a su vez contiene diferentes listas con los datos extraídos.
def limpiar_datos(lista):
    datos = []
    for elem in lista:
        datos.append(elem.strip().split(' '))
    return datos


# La función comienzo_deudas() se encarga de crear un diccionario en el que se almacena el nombre de cada inquilino como clave y su deuda como valor.
# Se toma el nombre de cada persona declarada en la primera linea del archivo y se le asigna una deuda de 0.
# Devuelve el diccionario con sus valores.
def comienzo_deudas(datos):
    deuda = {}
    for persona in datos[0]:
        deuda.update({persona: 0})
    return deuda


# La función calculo_deuda_por_dia() recibe una lista y un diccionario.
# Crea un diccionario llamado dias, en el que posteriormente se clasificará la evolución de las deudas en el tiempo.
# Para cada lista dentro de la lista recibida, toma el primer elemento y lo asigna a una variable fecha.
# Comprueba si el segundo valor es un '*', si hay un '~' dentro de la lista o si ninguna de estas condiciones se cumple.
# En el primer caso, el * nos indica que hay que agregar a una persona nueva al diccionario de deudas, cuya deuda inicial será 0.
# En el segundo caso, depende si el ~ se encuentra al final de la lista o no.
#   Si lo está, significa que la deuda le corresponde a todos los inquilinos y se procede a hacer el cálculo.
#   Si no está al final, significa que hay alguna/s persona/s a la/s que no le corresponde pagar la deuda. Estas personas no se toman en cuenta a la hora del cálculo.
# Si no se cumple nada de esto, podemos pensar que la deuda le corresponde solo a las personas indicadas. Solo se tiene en cuenta a los inquilinos que aparecen luego del monto para realizar los cálculos.
# Al diccionario dias, creado previamente, se le incorpora en cada iteración un par clave-valor, cuya clave es la fecha y el valor es el estado del diccionario de deudas en aquel momento.
# Devuelve el diccionario dias completo, luego de todas las operaciones.
def calculo_deuda_por_dia(datos, deuda):
    dias = {}
    fechas = []
    deudas = []
    deuda_anterior = deuda.copy()
    for linea in datos:
        nueva_deuda = deuda_anterior.copy()
        fecha = linea[0]
        if linea[1] == '*':
            # Incorporación de un nuevo inquilino: Primero esta la fecha, luego un asterisco que indica que se está sumando alguien, y luego el nombre del la persona que se suma.
            nueva_deuda.update({linea[2]: 0})
        elif '~' in linea:
            monto = int(linea[2])
            if linea[-1]=='~':
                # Deuda repartida entre todos: Primero esta la fecha, luego el que pagó y luego el monto.
                # Como ahora la deuda le corresponde a todos, en vez de poner los nombres de todos se pone específicamente el caracter ~.
                nueva_deuda[linea[1]] -= monto
                for persona in nueva_deuda:
                    nueva_deuda[persona] += monto/len(nueva_deuda)
            else:
                # Deuda repartida entre todos menos algunos: Primero esta la fecha, luego el que pagó y luego el monto.
                # Como la deuda le corresponde a todos menos algunos se agrega el ~ y luego los nombres de aquellos que no deben pagar esta deuda.
                nueva_deuda[linea[1]] -= monto
                no_debe = []
                for i in range(linea.index('~') + 1, len(linea)):
                    no_debe.append(linea[i])
                for persona in nueva_deuda:
                    if persona not in no_debe:
                        nueva_deuda[persona] += monto/(len(nueva_deuda)-len(no_debe))
        else:
            # Deuda repartida entre algunos: Primero esta la fecha, luego el que pagó, luego el monto, y luego a los que les corresponde la deuda
            monto = int(linea[2])
            nueva_deuda[linea[1]] -= monto
            corresponde = []
            for i in range(3, len(linea)):
                corresponde.append(linea[i])
            for persona in nueva_deuda:
                if persona in corresponde:
                    nueva_deuda[persona] += monto/len(corresponde)
        fechas.append(fecha)
        deudas.append(nueva_deuda)
        deuda_anterior = nueva_deuda.copy()
    dias = {fechas[i]: deudas[i] for i in range(len(fechas))}
    return dias


def datos_ordenados(nombre_archivo):
    # Todo el contenido del archivo de texto se almacena en la variable archivo
    archivo = leer_txt(nombre_archivo)
    # Se limpia y da formato a la información extraída previamente, para poder trabajar con ella
    datos_extraidos = limpiar_datos(archivo)
    # Se inician las deudas de todos los inquilinos originales en 0
    deuda = comienzo_deudas(datos_extraidos)
    # Saco la lista inicial de inquilinos, que ya fue almacenada en el diccionario de deudas, para quedarme solamente con los pagos realizados en cada fecha
    datos_extraidos.pop(0)
    # Almaceno el estado de las deudas de cada inquilino clasificado por fecha, dentro de la variable seguimiento_deudas
    seguimiento_deudas = calculo_deuda_por_dia(datos_extraidos, deuda)
    # Devuelvo seguimiento_deudas
    return seguimiento_deudas


# Una función que reciba el nombre de un archivo de transacciones y una fecha:
# 1. Si la fecha es anterior a la primer fecha del archivo, debe imprimir por pantalla que la fecha ingresada no es válida
# 2. Caso contrario, se deben hacer dos gráficos circulares con información correspondiente a la fecha ingresada.
#    El primer gráfico con aquellos a los que se les debe plata, y el segundo con aquellos que deben plata.
#    Para cada pedazo del círculo se debe informar el nombre y la deuda (para mejorar la legibilidad se debe poner el valor de las deudas con comillas).
#    Si la fecha seleccionada no registra transacciones, aun asi hay deudas. En esos casos deberá hacer los gráficos con las deudas de la fecha con transacciones más cercana (en el pasado).
def graficos_circulares(nombre_archivo, fecha):
    evolucion_deudas = datos_ordenados(nombre_archivo)
    fechas = list(evolucion_deudas.keys())
    fechas_int = []
    fecha_int = int(fecha.replace("-", ""))
    for elem in fechas:
        fechas_int.append(int(elem.replace("-", "")))
    if fecha_int < min(fechas_int):
        print("La fecha ingresada no es válida")
    else:
        if fecha_int not in fechas_int:
            temp = fecha_int
            for i in fechas_int:
                if temp > i:
                    fecha_int = i
            fecha = fechas[fechas_int.index(fecha_int)]
            
        deudas_de_la_fecha = evolucion_deudas[fecha]
        debe_label = []
        le_deben_label = []
        debe = []
        le_deben = []
        
        for inquilino, deuda in deudas_de_la_fecha.items():
            if deuda < 0:
                le_deben_label.append(inquilino + "\n$" + str(round(deuda, 2)))
                le_deben.append(abs(deuda))
            else:
                debe_label.append(inquilino + "\n$" + str(round(deuda, 2)))
                debe.append(deuda)
                
        #gráfico circular 1:
        y = np.array(debe)
        mylabels = debe_label
        plt.subplot(1, 3, 1)
        plt.pie(y, labels = mylabels)
        plt.title("Esta gente debe plata")

        #gráfico circular 2:
        y = np.array(le_deben)
        mylabels = le_deben_label
        plt.subplot(1, 3, 3)
        plt.pie(y, labels = mylabels)
        plt.title("A esta gente le deben plata")
        plt.show()


# Una función que reciba el nombre de un archivo de transacciones y haga un gráfico de la evolución de las deudas.
# El eje X serían las fechas, y el eje Y sería la deuda en pesos de cada persona.
# Debería haber una línea por persona. Si una persona se suma en el medio, su línea de deuda debe aparecer únicamente después de su primer deuda.
# Para que esté más "limpio" el eje X, solo se deben poner la primer y última fecha.
def grafico_evolucion_deudas(nombre_archivo):
    evolucion_deudas = datos_ordenados(nombre_archivo)
    fechas = list(evolucion_deudas.keys())
    deudas_en_fecha = []
    deudas_inquilino = {}
    fechas_inquilino = {}

    for fecha in fechas:
        for inquilino in evolucion_deudas[fecha]:
            deudas_inquilino[inquilino] = []
            fechas_inquilino[inquilino] = []
    for fecha in fechas:
        for inquilino in evolucion_deudas[fecha]:
            deudas_inquilino[inquilino].append(evolucion_deudas[fecha][inquilino])
            fechas_inquilino[inquilino].append(fecha)
    
    inquilinos = list(deudas_inquilino.keys())

    plt.figure()
    x = []
    y = []

    for inquilino in inquilinos:
        x = fechas_inquilino[inquilino]
        y = deudas_inquilino[inquilino]
        plt.plot(x, y, label = inquilino)
    
    plt.xticks([fechas[0], fechas[-1]], visible=True, rotation="horizontal")
    plt.title('Evolución de las deudas')
    plt.legend(loc='lower left')
    plt.show()
    




# PRUEBA DEL CODIGO

graficos_circulares("transacciones_largo.txt", "2023-03-05")
grafico_evolucion_deudas("transacciones_largo.txt")










