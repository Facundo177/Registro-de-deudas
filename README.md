<div align="center">
  <h1 align="center">
    Registro de deudas
  </h1>


## Introducción

<p>Este trabajo se centra en la contabilidad de una vivienda con múltiples inquilinos. 
  Se registra y almacena información sobre los gastos comunes realizados por los inquilinos en nombre de una o más personas. 
  El objetivo es analizar la evolución de las deudas de cada persona con la vivienda a lo largo del tiempo mediante la lectura, reestructuración y representación gráfica de los datos.
  Toda información relevante se encuentra almacenada en un archivo de texto, en un formato específico.
</p>

</div>
</br>

### Formato del archivo de texto

- La primer línea tiene los nombres de los inquilinos "originales", con los que se comienza el registro.
- Se pueden incorporar nuevos inquilinos:
  en una nueva línea, primero se registra la fecha, luego un asterisco (*) que indica que se está sumando alguien, y el nombre de esa persona.
- Se puede registrar una transacción a nombre de algunos:
  en una nueva línea, primero se registra la fecha, luego el que pagó, luego el monto, y luego a los que les corresponde la deuda, incluyendo a la persona que pagó (si corresponde).
- Se puede poner una deuda a nombre de todos:
  en una nueva línea, primero se registra la fecha, luego el que pagó y luego el monto. Para indicar que la deuda le corresponde a todos, se pone solamente el caracter ~.
- Se puede indicar que la deuda le corresponde a todos menos a algunos:
  en una nueva línea, primero se registra la fecha, luego el que pagó y luego el monto. Le sigue el ~ y luego los nombres de aquellos que no deben pagar esta deuda.
- Los pagos se toman como deuda negativa.

</br>

## Cómo funciona

Hay dos funciones creadas para realizar la visualización de datos:

### Consulta en un día específico

Se usa un gráfico de torta para representar el estado de deudas acumuladas en ese día en específico:
![image](https://github.com/user-attachments/assets/c8cc9284-557e-41d6-9ec4-268162b674f9)
(ejemplo del estado de deudas en el 2023-03-05)

### Evolución de deudas

Se grafica la evolución de las deudas día a día, desde el primer registro hasta el último:
![image](https://github.com/user-attachments/assets/ea5150b0-845d-4557-9982-e93f46e945de)

</br>


## Tecnologías aplicadas

Ejercicio realizado en Python:
- Uso de librerías como MatplotLib y Numpy para la representación de datos
- Manipulación de archivos
- Aplicación de estructuras de datos adecuadas al problema






