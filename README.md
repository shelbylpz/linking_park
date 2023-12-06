# Linking Park

Linking Park es un programa para la ayuda de gestión de un estacionamiento pequeño o Valet Parking. Este contiene funcionalidades como:
* Visualización de Entradas y Salidas.
* Configuración de Lugares.
* Sistema de Usuarios con distintos roles.
* Sistema de Cobro.
* Plantilla de Boleto imprimible
* Sistema de Boletaje y Asignación de Lugares Aleatorio.

## Requisitos del Sistema
#### Para la correcta instalación de este programa es necesario contar con los siguientes requisitos:
* Sistema Operativo Windows o Linux.
* Python 11.4+
* 2 GB RAM mínimos libres 
* 3 GB de espacio de almacenamiento
#### En caso de querer instalar la base de datos de manera local:
* 6 GB RAM
* 10 GB de espacio de almacenamiento

## Instalación
### Instalacion Automatica con .bat
* Una vez cumplidos los Requisitos del Sistema, solo será necesario descargar el archivo .bat del sistema operativo deseado encontrados en la raíz del repositorio. 
* Luego de descargar tenemos que verificar que el terminal puede [ejecutar Scripts](https://www.drupaladicto.com/snippet/como-habilitar-la-ejecucion-de-scripts-para-powershell) (Esto solo si esta en Windows). 
* Una vez activado esto procederemos a ejecutar el archivo .bat descargado. Y este clonara el repo e instalara el programa. En caso de fallar la activación del Virtuan Env, Cancelar el .bat con `CTRL + C` y proceder a una activacion manual en el punto .
* Si concluyo la instalacion y activacion del programa solo debe buscar en el navegador de su preferencia la ruta [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Instalacion Manual:
* Para la instalación Manual puede usar el .bat y detenerlo al intentar Activar el Entorno Virtual.
* De lo contrario, Clone el repositorio.
* Inicie una terminal y escriba los siguientes comandos:
```bash
# Ingrese a la ruta donde clono el repo ejemplo:
$ cd C:/users/my_user/downloads/linking_park

# Instale la libreria VritualEnv
$ python -m pip install virtualenv

# Una vez instalada cree un Entorno Virtual
$ python -m venv example-venv

# Una vez finalizada la creacion del Entorno Virtual se necesita activar.
$ & ./linking_park/example-venv/Scripts/Activate.ps1

# Una vez activado podemos instalar los requerimentos.
$ python -m pip install -r requirements.txt

# Una vez terminado podemos iniciar el programa e ingresar a la ruta del paso final de la instalacion automatica
$ python app/__init__.py 

#Instalacion Finalizada.

```
## Desarrolladores

* Alberto Demian Lopez Vazquez
* Cesar Daniel Gonzalez Giron
* Samuel Osvaldo Ramirez Cuenca
* Aranza Vanessa Perez Navarro
* Juan Manuel Vazquez Santillan
* Roberto Castro Ramirez
### El proyecto sigue en desarrollo..
