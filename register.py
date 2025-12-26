# -*- coding: utf-8 -*-

import cv2
import os
import time

# Configurações
MAX_IMAGES = 20  # Número máximo de fotos por usuário
DELAY_BETWEEN_SAVES = 1  # Tempo mínimo entre salvamentos em segundos

# Cria a pasta dataset se não existir
os.makedirs("dataset", exist_ok=True)

# Solicita o nome e matrícula do usuário
nome = input('Entre com seu nome: ')
matricula = input('Entre com sua matrícula: ')

# Armazena o nome e matrícula no arquivo de labelmap
with open("labelmap.csv", "a", encoding="utf-8") as file:
    file.write(f"{matricula},{nome}\n")

# Carrega o Detector de Face
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Pausa até o usuário apertar Enter
input("Pressione Enter para iniciar a captura de imagens...")

# Inicializa a captura da câmera
cam = cv2.VideoCapture(0)
img_counter = 0
last_save_time = time.time()

while img_counter < MAX_IMAGES:
    ret, frame = cam.read()
    if not ret:
        print("Falha ao capturar imagem da câmera")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta faces
    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        # Nenhuma face detectada: mostra mensagem na tela
        cv2.putText(frame, "Face nao detectada", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        # Desenha retângulo na primeira face detectada
        x, y, w, h = faces[0]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Salva a imagem automaticamente se passou DELAY_BETWEEN_SAVES segundos
        current_time = time.time()
        if current_time - last_save_time >= DELAY_BETWEEN_SAVES:
            face_gray = gray[y:y+h, x:x+w]
            filename = f"dataset/user-{matricula}-{img_counter}.jpg"
            cv2.imwrite(filename, face_gray)
            img_counter += 1
            last_save_time = current_time
            print(f"Imagem gravada: {filename}")

    # Mostra a quantidade de fotos já gravadas
    cv2.putText(frame, f"Fotos: {img_counter}/{MAX_IMAGES}", (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Exibe a imagem
    cv2.imshow("Coletor de Imagens Automático", frame)

    if cv2.waitKey(1) % 256 == 27:  # ESC para sair
        print("Saindo...")
        break

print(f"Meta de {MAX_IMAGES} fotos atingida!")
cam.release()
cv2.destroyAllWindows()
