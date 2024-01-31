from modulos.registro import Registro
from time import sleep
from modulos.registro_anterior import *


def funcao_encerrar_externamente(signum, frame):
    Registro.encerrar_programa()


# Registrar a função para ser chamada em caso de sinal de interrupção (Ctrl+C) ou término (fechar a janela)
signal.signal(signal.SIGINT, funcao_encerrar_externamente)
signal.signal(signal.SIGTERM, funcao_encerrar_externamente)


def exibir_nome_programa():
    Registro.limpar_tela()
    Registro.cor('=' * 30, 'ciano')

    Registro.cor(f'{"Cliente Register":^30}', 'ciano')

    Registro.cor('=' * 30, 'ciano')

def menu_de_opcoes():
    print('''
(1) Registrar novo cliente
(2) Listar clientes
(3) Retirar dinheiro do caixa 
(4) Fechar caixa
(5) Olhar registros anteriores                
(6) Sair          
          ''')

def voltar_ao_menu():
    input('\nPressione ENTER para voltar.')
    main()

def escolher_opcoes():
    opcao = Registro.validar_opcao_escolhida()
    
    if opcao == 1:
        Registro.validar_registro()
        voltar_ao_menu()

    elif opcao == 2:
        Registro.listar_clientes()
        main()
    
    elif opcao == 3:
        Registro.retirar_dinheiro_do_caixa()
        voltar_ao_menu()

    elif opcao == 4:
        Registro.fechar_caixa()
        main()

    elif opcao == 5:
        main2()
        main()

    elif opcao == 6:
        Registro.encerrar_programa()

    else:
        main()

def main():
    exibir_nome_programa()
    menu_de_opcoes()
    escolher_opcoes()

if __name__ == '__main__':
    main()