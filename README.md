Por implementar:
- Dejar la interfaz más bonita visualmente
- Dejar codigo base de datos (dejar camino para posibles implementaciones)
- Compilar codigo para enviar .exe
- Crear carpetas para separar las cosas (excel del codigo, imagenes del código...)

# Proyecto: PPG-Project

## Descripción  
Este proyecto es una aplicación de escritorio para poder administrar lotes de pinturas dado un archivo Excel. Consta de una interfaz gráfica para poder ver la distribución de los lotes en un mes elegido. También tiene implementado la capacidad de visualizar los dias festivos para poder hacer una mejor estimación de donde acabarían los productos realizados. 

## Requisitos Previos
Antes de ejecutar el proyecto, asegúrate de contar con algo de lo siguiente:

### Ejecución a traves de código
Este código ha sido creado, implementado y probado en la versión `Python 3.12.3`. Para poder instalar las dependencias que tiene el código, tenemos que ejecutar el siguiente comando en la terminal:
```bash
$ pip3 install -r requirements.txt
```
Una vez instaladas las librerias necesarias, vamos a ejecutar el siguiente comando en una terminal:
```bash
$ python3 Interfaz.py
```

### Ejecución a traves de un ejecutable (.exe)
En este caso, no vamos a necesitar instalar ninguna dependencia ya que el código ha sido compilado con las propias librerias, por lo que no es necesario ningun tipo de paso adicional. Simplemente hacemos doble clic en el ejecutable y ya se abriría.

## Uso de la aplicación
### Inicio de la aplicación
Nada más ejecutar la aplicación, saldrá una ventana con dos botones principales:
- El botón `Añadir nuevo lote` crea una nueva interfaz que permite añadir nuevos productos al Excel al final de este para evitar tener que ejecutar la aplicación de Excel de Microsoft.
- El botón `Iniciar aplicación` crea una nueva intefaz en el que aparecerá una pantalla en blanco. Una vez elegido en el desplegable el mes que quiere visualizar, podrá ver la asignación de los lotes del Excel dado. Hablaremos con más detalle más adelante.
- Un botón `i` para mostrar información sobre la aplicación, que versión tiene y otro tipo de información ajena a ella.

### Despliegue de los lotes
Una vez iniciado la interfaz del botón `Iniciar aplicación`, vamos a tener que elegir el mes en el que estamos en la esquina inferior derecha. Una vez escogido el mes, vamos a poder ver 4 botones abajo izquierda que representan las cuatro plantas que tiene la empresa. A partir de ahí, vamos a poder ver como están distribuidos los lotes en base a su fecha requerida y lo que tarda en realizarse ese lote.

Además, hemos representado los diferentes dias no laborales para poder crear una mejor visualización de como van a tener que ser realizados los diferentes lotes. Estos dias van a estar pintados de color gris siempre para evitar confundirnos con otro tipo de pinturas.

## Posibles mejoras al código
Algunas de las posibles mejoras que contemplamos como equipo serían:
- Una mejora del tiempo de ejecución del algoritmo de Backtracking para la elección de lotes de la manera más óptima.
- Una limpieza más profunda del código para reutilizar el código.
- Mejora visual de la interfaz de usuario.
- En caso de necesitar un sistema de autenticación, implementarlo en la primera interfaz.

## Contribuidores al código
- [Nombre 1 - Rol]
- [Nombre 2 - Rol]
- [Nombre 3 - Rol]
- [Nombre 4 - Rol]