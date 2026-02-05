# -*- coding: utf-8 -*-
# Define a codificação do arquivo como UTF-8, permitindo acentos e caracteres especiais.

import cv2
# Importa a biblioteca OpenCV, usada para processamento de imagens e visão computacional.

import os
# Importa a biblioteca padrão para manipulação de arquivos e diretórios.

import numpy as np
# Importa o NumPy, usado para manipulação de arrays numéricos.

from PIL import Image
# Importa a biblioteca Pillow (PIL), usada para abrir e manipular imagens.

# Configurações
DATASET_PATH = 'dataset'
# Define o caminho da pasta onde estão as imagens do dataset.

FACE_SIZE = (200, 200)  # tamanho padronizado
# Define o tamanho fixo (200x200 pixels) para redimensionar as faces detectadas.

# Carrega o Detector de Face
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Carrega o classificador Haar Cascade pré-treinado para detectar faces frontais.

def limpar_e_redimensionar_dataset_inplace(path, face_size=(200, 200)):
    # Função que percorre todas as imagens do dataset, detecta faces e redimensiona.

    imagens = [f for f in os.listdir(
        path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    # Lista todos os arquivos da pasta que terminam com extensões de imagem válidas.

    contador_total = 0
    # Contador de imagens processadas (total).

    contador_face = 0
    # Contador de imagens que tiveram uma face detectada e foram mantidas.

    for imagem_nome in imagens:
        # Loop para percorrer cada imagem encontrada no dataset.

        contador_total += 1
        # Incrementa o contador de imagens totais.

        caminho_imagem = os.path.join(path, imagem_nome)
        # Cria o caminho completo da imagem (pasta + nome do arquivo).

        try:
            img = Image.open(caminho_imagem).convert('L')  
            # Abre a imagem e converte para escala de cinza (grayscale).

            img_array = np.array(img, 'uint8')
            # Converte a imagem para um array NumPy de inteiros de 8 bits.

            faces_detectadas = detector.detectMultiScale(
                img_array, scaleFactor=1.1, minNeighbors=3)
            # Detecta faces na imagem usando o classificador Haar Cascade.
            # scaleFactor: controla o tamanho da janela de busca.
            # minNeighbors: número mínimo de vizinhos para validar uma detecção.

            if len(faces_detectadas) == 0:
                # Se nenhuma face foi encontrada:

                print(f"Nenhuma face detectada: {imagem_nome}, removendo arquivo.")
                # Exibe mensagem informando que não foi detectada face.

                os.remove(caminho_imagem)  
                # Remove a imagem do dataset por não conter face.

                continue
                # Pula para a próxima imagem.

            # Pega apenas a primeira face detectada
            x, y, w, h = faces_detectadas[0]
            # Extrai as coordenadas da primeira face encontrada (x, y, largura, altura).

            face_roi = img_array[y:y+h, x:x+w]
            # Recorta a região da face (ROI = Region of Interest).

            # Redimensiona para tamanho padronizado
            face_resized = cv2.resize(face_roi, face_size)
            # Redimensiona a face recortada para 200x200 pixels.

            # Substitui a imagem original
            cv2.imwrite(caminho_imagem, face_resized)
            # Salva a face redimensionada sobrescrevendo o arquivo original.

            contador_face += 1
            # Incrementa o contador de imagens válidas (com face).

        except Exception as e:
            # Caso ocorra algum erro durante o processamento:

            print(f"Erro ao processar {imagem_nome}: {e}")
            # Exibe mensagem com o erro.

    print(f"Processamento concluído! {contador_face}/{contador_total} imagens mantidas e redimensionadas.")
    # Exibe resumo final: quantas imagens foram mantidas e redimensionadas.

# Executa a limpeza e redimensionamento inplace
limpar_e_redimensionar_dataset_inplace(DATASET_PATH, FACE_SIZE)
# Chama a função passando o caminho do dataset e o tamanho padrão das faces.
