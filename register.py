# -*- coding: utf-8 -*-
# Define a codificação do arquivo como UTF-8, permitindo acentos e caracteres especiais.

import cv2
# Importa a biblioteca OpenCV, usada para captura de vídeo e processamento de imagens.

import os
# Importa a biblioteca padrão para manipulação de arquivos e diretórios.

import time
# Importa a biblioteca padrão para trabalhar com tempo (delays, timestamps).

# Configurações
MAX_IMAGES = 20  # Número máximo de fotos por usuário
DELAY_BETWEEN_SAVES = 1  # Tempo mínimo entre salvamentos em segundos

# Cria a pasta dataset se não existir
os.makedirs("dataset", exist_ok=True)
# Garante que a pasta "dataset" exista; se não existir, cria automaticamente.

# Solicita o nome e matrícula do usuário
nome = input('Entre com seu nome: ')
# Pede ao usuário digitar seu nome.

matricula = input('Entre com sua matrícula: ')
# Pede ao usuário digitar sua matrícula.

# Armazena o nome e matrícula no arquivo de labelmap
with open("labelmap.csv", "a", encoding="utf-8") as file:
    file.write(f"{matricula},{nome}\n")
# Abre (ou cria) o arquivo "labelmap.csv" e adiciona uma linha com matrícula e nome.

# Carrega o Detector de Face
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Carrega o classificador Haar Cascade pré-treinado para detectar faces frontais.

# Pausa até o usuário apertar Enter
input("Pressione Enter para iniciar a captura de imagens...")
# Espera o usuário confirmar antes de começar a captura.

# Inicializa a captura da câmera
cam = cv2.VideoCapture(0)
# Abre a câmera padrão (índice 0).

img_counter = 0
# Contador de imagens já salvas.

last_save_time = time.time()
# Marca o tempo da última imagem salva (inicialmente o tempo atual).

while img_counter < MAX_IMAGES:
    # Loop que roda até atingir o número máximo de imagens.

    ret, frame = cam.read()
    # Captura um frame da câmera.

    if not ret:
        print("Falha ao capturar imagem da câmera")
        break
    # Se não conseguiu capturar, mostra erro e encerra.

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Converte o frame para escala de cinza (necessário para detecção de faces).

    # Detecta faces
    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    # Detecta faces na imagem em escala de cinza.
    # scaleFactor: controla o tamanho da janela de busca.
    # minNeighbors: número mínimo de vizinhos para validar uma detecção.

    if len(faces) == 0:
        # Nenhuma face detectada: mostra mensagem na tela
        cv2.putText(frame, "Face nao detectada", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # Escreve "Face nao detectada" em vermelho na tela.
    else:
        # Desenha retângulo na primeira face detectada
        x, y, w, h = faces[0]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Desenha um retângulo azul em volta da face detectada.

        # Salva a imagem automaticamente se passou DELAY_BETWEEN_SAVES segundos
        current_time = time.time()
        if current_time - last_save_time >= DELAY_BETWEEN_SAVES:
            face_gray = gray[y:y+h, x:x+w]
            # Recorta apenas a região da face em escala de cinza.

            filename = f"dataset/user-{matricula}-{img_counter}.jpg"
            # Define o nome do arquivo com matrícula e número da foto.

            cv2.imwrite(filename, face_gray)
            # Salva a imagem da face recortada no dataset.

            img_counter += 1
            # Incrementa o contador de imagens salvas.

            last_save_time = current_time
            # Atualiza o tempo da última imagem salva.

            print(f"Imagem gravada: {filename}")
            # Mostra no terminal que a imagem foi salva.

    # Mostra a quantidade de fotos já gravadas
    cv2.putText(frame, f"Fotos: {img_counter}/{MAX_IMAGES}", (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # Escreve na tela quantas fotos já foram salvas.

    # Exibe a imagem
    cv2.imshow("Coletor de Imagens Automático", frame)
    # Mostra o frame com as informações e retângulo da face.

    if cv2.waitKey(1) % 256 == 27:  # ESC para sair
        print("Saindo...")
        break
    # Se o usuário apertar ESC, encerra o loop.

print(f"Meta de {MAX_IMAGES} fotos atingida!")
# Mensagem final quando o número máximo de fotos é atingido.

cam.release()
# Libera a câmera.

cv2.destroyAllWindows()
# Fecha todas as janelas abertas pelo OpenCV.
