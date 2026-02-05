# -*- coding: utf-8 -*-
# Define a codificação do arquivo como UTF-8, permitindo acentos e caracteres especiais.

# Importando as bibliotecas necessárias.
import sys, os
# sys: usado para encerrar o programa com sys.exit().
# os: usado para executar comandos do sistema, como limpar a tela.

import subprocess
# subprocess: usado para chamar outros scripts Python (register.py, train.py, recognition.py).

# Menu principal
def main_menu():
    os.system('clear')
    # Limpa a tela do terminal (em sistemas Linux/Unix).

    print("SISTEMA DE RECONHECIMENTO FACIAL - OPENCV\n")
    # Exibe o título do sistema.

    print("Escolha a tarefa para iniciar:")
    print("1. Registrar novo usuário")
    print("2. Treinar o algoritmo LBPH")
    print("3. Identificacao facial")
    print("\n0. Sair")
    # Mostra as opções disponíveis no menu principal.

    choice = input(" >>  ")
    # Lê a escolha do usuário.

    exec_menu(choice)
    # Chama a função que executa a opção escolhida.

    return

# Executa o menu selecionado
def exec_menu(choice):
    os.system('clear')
    # Limpa a tela novamente.

    ch = choice.lower()
    # Converte a escolha para minúsculas (para evitar problemas de maiúsculas/minúsculas).

    if ch == '':
        # Se o usuário não digitou nada, volta ao menu principal.
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
            # Tenta executar a função correspondente à escolha do usuário.
        except KeyError:
            # Se a escolha não existe no dicionário menu_actions:
            print("Menu inválido, tente novamente.\n")
            menu_actions['main_menu']()
            # Exibe mensagem de erro e retorna ao menu principal.
    return

# Menu 1
def menu1():
    print("Entre com os dados para registrar o usuario:\n")
    # Exibe instrução para registrar novo usuário.

    subprocess.call(["python", "register.py"])
    # Executa o script register.py, responsável por coletar dados e imagens do usuário.

    print("9. Voltar")
    print("0. Sair")
    # Exibe opções após terminar o registro.

    choice = input(" >>  ")
    exec_menu(choice)
    # Lê a escolha e executa o menu correspondente.
    return

# Menu 2
def menu2():
    print("Treinando o algoritmo...\n")
    # Exibe mensagem de treinamento.

    subprocess.call(["python", "train.py"])
    # Executa o script train.py, responsável por treinar o modelo LBPH com as imagens coletadas.

    print("9. Voltar")
    print("0. Sair" )
    # Exibe opções após o treinamento.

    choice = input(" >>  ")
    exec_menu(choice)
    # Lê a escolha e executa o menu correspondente.
    return

# Menu 3
def menu3():
    print("Reconhecimento Facial\n")
    # Exibe mensagem de início do reconhecimento.

    subprocess.call(["python", "recognition.py"])
    # Executa o script recognition.py, responsável por identificar usuários com base no modelo treinado.

    print("9. Voltar")
    print("0. Sair")
    # Exibe opções após o reconhecimento.

    choice = input(" >>  ")
    exec_menu(choice)
    # Lê a escolha e executa o menu correspondente.
    return

# Retorna ao menu principal
def back():
    menu_actions['main_menu']()
    # Função que retorna ao menu principal.

# Finaliza o programa
def exit():
    sys.exit()
    # Encerra a execução do programa.

# Opções e menus
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '9': back,
    '0': exit,
}
# Dicionário que mapeia cada opção do menu para a função correspondente.

# Menu Principal
if __name__ == "__main__":
    # Inicializa o Menu Principal
    main_menu()
    # Se o script for executado diretamente, inicia o menu principal.
