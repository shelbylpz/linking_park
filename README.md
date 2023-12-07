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

### Instalación Automatica en Linux
* Descargar el archivo .sh del repositorio
* Ejecutar .sh, lo cual clonará el repositorio e instalará el programa.
```bash
bash startLinux.sh
```
* Si concluyo la instalacion y activacion del programa solo debe buscar en el navegador de su preferencia la ruta [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Instalacion Manual Windows:
* Para la instalación Manual puede usar el .bat y detenerlo al intentar Activar el Entorno Virtual.
* De lo contrario, Clone el repositorio.
* Inicie una terminal y escriba los siguientes comandos:
```bat
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

### Instalación Manual Linux:
### Instalar python
#### Debian/Ubuntu
```bash
sudo apt update && sudo apt upgrade
sudo apt install python3 python3-venv
```
#### Redhat
```bash
yum -y install @development
yum -y install rh-python36
yum -y install rh-python3-venv
```
#### Nix package manager
[nix packages](https://search.nixos.org/packages?channel=unstable&show=python3&from=0&size=50&sort=relevance&type=packages&query=python)

### Instalar programa
```bash
# Clonar repositorio
git clone https://github.com/shelbylpz/linking_park.git

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar requerimentos
pip install -r requirements.txt

# Iniciar el programa
python3 app/__init__.py
```
## Notas de configuracion
* Para la impresion del ticket se tiene que tener previamente configurada la impresora donde se imprimiran los tickets, esta debe estar configurada como predeterminada en el sistema.
* El tamaño de hoja del ticket es el A7.
* La linea que imprime el ticket esta comentada por motivos de pruebas, la funcion en cuestion se llama `imprimirboleto()`, para hacer las impresiones es solo necesario descomentarla y comentar la linea que abre el boleto llamada `abrirboleto()`.
  
## Desarrolladores

* Alberto Demian Lopez Vazquez
* Cesar Daniel Gonzalez Giron
* Samuel Osvaldo Ramirez Cuenca
* Aranza Vanessa Perez Navarro
* Juan Manuel Vazquez Santillan
* Roberto Castro Ramirez
### El proyecto sigue en desarrollo..
