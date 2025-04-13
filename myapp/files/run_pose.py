import sys
from utils.gst_utils import gst_launch

# Configuración
DEVICE = "AUTO"
MODELS_PATH = "/home/dlstreamer/models"  # Esta ruta es DENTRO del contenedor
MODELS_PROC_PATH = "/home/dlstreamer/code/model_proc"  # Esta ruta es DENTRO del contenedor
MODEL_1 = "human-pose-estimation-0001"
HPE_MODEL_PROC = f"{MODELS_PROC_PATH}/{MODEL_1}.json"
HPE_MODEL = f"{MODELS_PATH}/intel/{MODEL_1}/FP32/{MODEL_1}.xml"
INPUT = "https://github.com/intel-iot-devkit/sample-videos/raw/master/face-demographics-walking.mp4"

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
