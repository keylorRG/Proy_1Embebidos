import cv2
import numpy as np
import subprocess
import shlex

def view_opencv(pipeline_str):
    """Visualiza el pipeline con OpenCV directamente"""
    cap = cv2.VideoCapture(pipeline_str, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        raise Exception("Error: Could not open GStreamer pipeline.")
    
    cv2.namedWindow("Pose Estimation", cv2.WINDOW_NORMAL)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        cv2.imshow("Pose Estimation", frame)
        
        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def gst_launch_direct(pipeline_str):
    """Ejecuta el pipeline directamente con gst-launch-1.0"""
    cmd = f"gst-launch-1.0 {pipeline_str}"
    print(f"Ejecutando: {cmd}")
    
    try:
        process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"Error en el pipeline: {stderr.decode()}")
            return False
        
        return True
    except Exception as e:
        print(f"Error al ejecutar el pipeline: {e}")
        return False

def gst_launch(pipeline_str):
    """Función principal que elige entre modo directo o modo OpenCV"""
    # Si el pipeline termina con autovideosink, usar gst-launch directamente
    if "autovideosink" in pipeline_str:
        return gst_launch_direct(pipeline_str)
    
    # Si necesitas procesamiento adicional, usar OpenCV
    try:
        view_opencv(pipeline_str)
        return True
    except Exception as e:
        print(f"Error al usar OpenCV: {e}")
        print("Intentando con gst-launch directo...")
        return gst_launch_direct(pipeline_str)
