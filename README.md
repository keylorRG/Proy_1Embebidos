# Documentacion - Tutorial
## Descripción: 

En este tutorial se documentan aspectos técnicos acerca del flujo de trabajo seguido para lograr implementar la imagen de Linux a la medida con Yocto Project para correr una aplicación desarrollada, capaz de ser ejecutada en un amaquina virtual corriendo sobre una arquitectura x86, partiendo de una imagen mínima de Yocto Project. 

### Computador Host

El proyecto fue desarrollado en un computador host con las siguientes características: 

Dar características.

### Características de los toolkits utilizados

Yocto Project: versión scarthgap.

90 Gbytes o más de espacio libre de memoria en disco, al menos 8 Gbytes de memoria RAM, sin embargo se recomienda tener tantos Gbytes de memoria RAM como cores tenga la computadora hos para mejorar el proceso. Tener un sistema operativo soportado (Fedora, openSUSE, CentOS, Debian, o Ubuntu) [1].

Ciertas dependencias de software: 

Git 1.8.3.1+, tar 1.28+, Python 3.8.0+, gcc 8.0+, GNU make 4.0+.

#### Docker 

Este toolkit fue utilizado como paso intermedio, previamente a la construccion de la imagen en Yocto Project para tener un escapsulado en el que se instalaran todas las dependencias necesarias y verificar el funcionamiento de la aplicación. La versión utilizada fue 28.0.2.

#### OpenVINO

La versión implementada en la aplicación sigue la versión 2023.3 con la guia oficial encontrada en [2].

#### Gstreamer

Dentro del archivo de configuración de Yocto Project fueron agregados plugins de Gstreamer bajo la versión 1.22.12.

#### Virtual Box

La imagen a medida finalmente se corrió en una máquina virtual usando VirtualBox.

#### Otros

Dentro de los toolkits necesarios para la aplicación está presente python3, mumpy y pillow. 

### Flujo de trabajo de los toolkits utilizados

Se revisó el ejemplo proporcionado en el taller de OpenVINO como referencia y punto de partida. Con estos recursos se tomaron como referencia y se generó un contenedor Docker. Se desarrolló un Dockerfile donde se describieron todas las dependencias y requerimientos tanto a nivel de software/toolkits así como del modelo a probar. 

Posteriormente se hizo la configuración inicial del entorno de Yocto Project y la verificación de sus requerimientos como se mencionó anteriormente. 
Se añadieron las layers correspondientes a OpenVINO, luego se modificó el archivo local.config para agregar Gstreamer. 

Se hizo una layer personalizada para agregar la aplicación a probar. 
Se intentó agregar una capa personalizada para agregar los elementos específicar de dlstreamer que no incluye gstreamer por defecto, sin embargo, este paso no fue éxitoso. 

Tras varios procesos de compilación se probó la correcta instalación tanto de OpenVINO, Gstreamer, la layer personalizada y se probó la aplicación con una modificación para que no dependiera de los elementos de dlstreamer (gvaclasify y gvawaterark).

Finalmente, se utilizí VirtualBox y se cargó la imagen de linux para correrlo en una maquina virtual. 

### Selección de la aplicación

La aplicación escogida para probar en la imagen de Linux se basó en el modelo llamado 'human-pose-estimation' a partir de un programa en python. 

```python
import sys
from utils.gst_utils import gst_launch

# Configuración
DEVICE = "AUTO"
MODELS_PATH = "ruta al modelo"
MODELS_PROC_PATH = "ruta al model_proc" 
MODEL_1 = "nombre del modelo"
HPE_MODEL_PROC = f"{MODELS_PROC_PATH}/{MODEL_1}.json"
HPE_MODEL = f"{MODELS_PATH}/intel/{MODEL_1}/FP32/{MODEL_1}.xml"
INPUT = "video fuente"

# Pipeline GStreamer
pipeline_str = (
    f'urisourcebin buffer-size=4096 uri={INPUT} ! '
    f'decodebin ! '
    #f'v4l2src !'
    #f'videoconvert !'
    f'gvaclassify model={HPE_MODEL} model-proc={HPE_MODEL_PROC} device={DEVICE} inference-region=full-frame ! queue ! '
    f'gvawatermark ! videoconvert ! autovideosink'
)
# Ejecutar la pipeline
print(f"Ejecutando pipeline de estimación de pose humana...")
gst_launch(pipeline_str)
```

Esta aplicación tiene dos partes principales: descripción de las rutas a buscar para encontrar todos los archivos necesarios y el pipeline a ejecutar por gstreamer. 
Como se puede observar, esta aplicación busca el nombre del modelo que se le diga, en este caso: human-pose-estimation. 

### Mapeo de dependencias

Las layers utilizadas son: 

1) meta-poky y core: proporcionan el sistema base de Linux, incluyen herramientas esenciales del sistema y bibliotecas base, además de que proveen el framework BitBake para la construcción de imágenes.

2) meta-intel: proporciona OpenVINO y sus componentes. 

3) meta-openembedded/meta-oe: incluye dependencias generales para multimedia e IA y ofrece bibliotecas de utilidad necesarias para procesamiento de imagen.

4) meta-openembedded/meta-python: proporciona módulos Python adicionales como numpy. 

5) meta-openembedded/meta-multimedia: bibliotecas adicionales para GStreamer y herramientas de procesamiento multimedia. 

6) meta-myapp: contiene la aplicación principal de detectión de pose humana, el video fuente y el modelo preentrenado. 

GStreamer (de poky/meta) utiliza OpenCV (de meta-oe), la capa que se intentó añadir dlstreamer (de meta-dlstreamer) depende de OpenVINO (de meta-intel). Y la aplicación principal (de meta-myapp) depende de todos los componentes anteriores.



## Referencias

[1] https://docs.yoctoproject.org/5.0.7/brief-yoctoprojectqs/index.html

[2] https://docs.openvino.ai/2023.3/openvino_docs_install_guides_installing_openvino_yocto.html


