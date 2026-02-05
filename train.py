<<<<<<< HEAD
# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np
from PIL import Image

# Configurações
DATASET_PATH = 'dataset'
FACE_SIZE = (200, 200)  # tamanho padronizado

# Carrega o Detector de Face
=======
# Define a codificação do arquivo como UTF-8, garantindo suporte a caracteres especiais (acentos, etc.).
# -*- coding: utf-8 -*-

# Importa a biblioteca OpenCV, usada para processamento de imagens e visão computacional.
import cv2

# Importa a biblioteca padrão para manipulação de arquivos e diretórios.
import os

# Importa o NumPy, usado para manipulação de arrays numéricos.
import numpy as np

# Importa a biblioteca Pillow (PIL), usada para abrir e manipular imagens.
from PIL import Image

# Define o caminho da pasta onde estão as imagens do dataset.
DATASET_PATH = 'dataset'

# Define o tamanho fixo (largura x altura) para redimensionar as faces detectadas.
FACE_SIZE = (200, 200)  # tamanho padronizado

# Carrega o classificador Haar Cascade pré-treinado para detecção de faces frontais.
>>>>>>> dd81839 ( atualizando projeto)
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


<<<<<<< HEAD
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

=======
# Define uma função que limpa e redimensiona as imagens do dataset no próprio local.
def limpar_e_redimensionar_dataset_inplace(path, face_size=(200, 200)):

    # Lista todos os arquivos da pasta que possuem extensão de imagem válida.
    imagens = [f for f in os.listdir(
        path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Contador de imagens processadas (total).
    contador_total = 0

    # Contador de imagens que tiveram uma face detectada e foram mantidas.
    contador_face = 0

    # Loop para percorrer cada imagem encontrada.
    for imagem_nome in imagens:

        # Incrementa o contador de imagens totais.
        contador_total += 1

        # Cria o caminho completo da imagem.
        caminho_imagem = os.path.join(path, imagem_nome)

        try:
            # Abre a imagem e converte para escala de cinza (grayscale).
            img = Image.open(caminho_imagem).convert('L')

            # Converte a imagem para um array NumPy com tipo de dado inteiro de 8 bits.
            img_array = np.array(img, 'uint8')

            # Detecta faces na imagem usando o classificador Haar Cascade.
            # scaleFactor: controla o tamanho da imagem em cada escala.
            # minNeighbors: número mínimo de vizinhos para validar uma detecção.
            faces_detectadas = detector.detectMultiScale(
                img_array, scaleFactor=1.1, minNeighbors=3)

            # Se nenhuma face for detectada:
            if len(faces_detectadas) == 0:

                # Exibe mensagem informando que não foi encontrada face.
                print(f"Nenhuma face detectada: {imagem_nome}, removendo arquivo.")

                # Remove a imagem do dataset.
                os.remove(caminho_imagem)

                # Pula para a próxima imagem.
                continue

            # Extrai as coordenadas da primeira face detectada (x, y, largura, altura).
            x, y, w, h = faces_detectadas[0]

            # Recorta a região da imagem correspondente à face.
            face_roi = img_array[y:y+h, x:x+w]

            # Redimensiona a face recortada para o tamanho definido (200x200).
            face_resized = cv2.resize(face_roi, face_size)

            # Salva a face redimensionada sobrescrevendo a imagem original.
            cv2.imwrite(caminho_imagem, face_resized)

            # Incrementa o contador de imagens válidas (com face).
            contador_face += 1

        # Caso ocorra algum erro durante o processamento:
        except Exception as e:

            # Exibe mensagem de erro.
            print(f"Erro ao processar {imagem_nome}: {e}")

    # Exibe resumo do processamento: quantas imagens foram mantidas e redimensionadas.
>>>>>>> dd81839 ( atualizando projeto)
    print(
        f"Processamento concluído! {contador_face}/{contador_total} imagens mantidas e redimensionadas.")


<<<<<<< HEAD
# Executa a limpeza e redimensionamento inplace
=======
# Chama a função para processar todas as imagens da pasta 'dataset'.
>>>>>>> dd81839 ( atualizando projeto)
limpar_e_redimensionar_dataset_inplace(DATASET_PATH, FACE_SIZE)
