# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np
from PIL import Image

# Configurações
DATASET_PATH = 'dataset'
FACE_SIZE = (200, 200)  # tamanho padronizado

# Carrega o Detector de Face
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def limpar_e_redimensionar_dataset_inplace(path, face_size=(200, 200)):
    imagens = [f for f in os.listdir(
        path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    contador_total = 0
    contador_face = 0

    for imagem_nome in imagens:
        contador_total += 1
        caminho_imagem = os.path.join(path, imagem_nome)
        try:
            img = Image.open(caminho_imagem).convert(
                'L')  # converte para grayscale
            img_array = np.array(img, 'uint8')

            faces_detectadas = detector.detectMultiScale(
                img_array, scaleFactor=1.1, minNeighbors=3)
            if len(faces_detectadas) == 0:
                print(
                    f"Nenhuma face detectada: {imagem_nome}, removendo arquivo.")
                os.remove(caminho_imagem)  # remove imagem sem face
                continue

            # Pega apenas a primeira face detectada
            x, y, w, h = faces_detectadas[0]
            face_roi = img_array[y:y+h, x:x+w]

            # Redimensiona para tamanho padronizado
            face_resized = cv2.resize(face_roi, face_size)

            # Substitui a imagem original
            cv2.imwrite(caminho_imagem, face_resized)
            contador_face += 1

        except Exception as e:
            print(f"Erro ao processar {imagem_nome}: {e}")

    print(
        f"Processamento concluído! {contador_face}/{contador_total} imagens mantidas e redimensionadas.")


# Executa a limpeza e redimensionamento inplace
limpar_e_redimensionar_dataset_inplace(DATASET_PATH, FACE_SIZE)
