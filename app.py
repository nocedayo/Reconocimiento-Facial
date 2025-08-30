import cv2
import os
import face_recognition
from datetime import datetime
import csv

# --- Carpeta de referencia ---
carpeta_fotos = "data"
codificaciones_conocidas = []
nombres_referencia = []
# Carpeta donde guardar las capturas
carpeta_capturas = "capturas"
os.makedirs(carpeta_capturas, exist_ok=True)    

# Cargar las codificaciones de las caras de referencia
for archivo in os.listdir(carpeta_fotos):
    if archivo.endswith(("jpg", "png", "jpeg")):
        ruta_completa = os.path.join(carpeta_fotos, archivo)
        imagen = face_recognition.load_image_file(ruta_completa)
        
        # Asume que hay solo una cara por foto de referencia
        codificaciones = face_recognition.face_encodings(imagen)
        if len(codificaciones) > 0:
            codificaciones_conocidas.append(codificaciones[0])
            nombres_referencia.append(os.path.splitext(archivo)[0])

# --- Encender cámara ---
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break
    
    # Redimensionar el frame para acelerar el procesamiento
    frame_pequeno = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    
    # Encontrar todas las caras y sus codificaciones en el frame actual
    ubicaciones_caras = face_recognition.face_locations(frame_pequeno)
    codificaciones_caras = face_recognition.face_encodings(frame_pequeno, ubicaciones_caras)
    
    # Comparar las codificaciones del frame con las de referencia
    for codificacion_cara, ubicacion_cara in zip(codificaciones_caras, ubicaciones_caras):
        coincidencias = face_recognition.compare_faces(codificaciones_conocidas, codificacion_cara)
        nombre_detectado = "Desconocido"
      

        
        if True in coincidencias:
            primer_coincidencia_indice = coincidencias.index(True)
            nombre_detectado = nombres_referencia[primer_coincidencia_indice]
        
        # Escalar las coordenadas del rostro a su tamaño original
        y1, x2, y2, x1 = ubicacion_cara
        y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2
        
           # Guardar en log si se reconoce
        if nombre_detectado != "Desconocido":
            hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with open("registro.txt", "a") as f:
                f.write(f"{nombre_detectado}-{hora_actual}\n")

            # Guardar la foto del rostro reconocido
            nombre_archivo = f"{nombre_detectado}_{hora_actual}.jpg"
            ruta_archivo = os.path.join(carpeta_capturas, nombre_archivo)
            cv2.imwrite(ruta_archivo, frame)  # Guarda todo el frame
            #cv2.imwrite(ruta_archivo, rostro)  # Guarda solo el rostro recortado


        # Dibujar rectángulo y texto
        color = (0, 255, 0) if nombre_detectado != "Desconocido" else (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, nombre_detectado, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # Mostrar la ventana
    cv2.imshow("Reconocimiento Facial", frame)

    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

cam.release()
cv2.destroyAllWindows()