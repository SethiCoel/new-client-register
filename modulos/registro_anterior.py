from modulos.registro import *

data_escolhida_global = ''

ciclo_ativo = True

def funcao_encerrar_externamente(signum, frame):
    Registro.encerrar_programa()


# Registrar a função para ser chamada em caso de sinal de interrupção (Ctrl+C) ou término (fechar a janela)
signal.signal(signal.SIGINT, funcao_encerrar_externamente)
signal.signal(signal.SIGTERM, funcao_encerrar_externamente)


def registro_anterior():
    while True:

        Registro.sub_titulo('Registros Anteriores')
    
        tabelas = cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name NOT LIKE ?', (f'valor_%',)).fetchall()

        print(f'{"ID":<10}  Data')
        print('-'*30)
        for id, tabela in enumerate(tabelas):
            print(f'{id:<10}  {tabela[0]}')

        print('\n\nPressione ENTER para voltar.')
        
        escolha_id = input('Digite o ID da data que deseja ver: ')
        
        if escolha_id == '':
            global ciclo_ativo
            ciclo_ativo = False
            break
        
        try:

            escolha_id = int(escolha_id)

            if 0 <= escolha_id < len(tabelas):
                
                ciclo_ativo = True
                data_escolhida = tabelas[escolha_id][0]

                global data_escolhida_global

                data_escolhida_global = data_escolhida
                
                cursor.execute(f'SELECT * FROM "{data_escolhida}"')
                cursor.execute(f'SELECT * FROM "valor_{data_escolhida}"')
            break
        

        except Exception as error:
            Registro.sub_titulo(f'Registros Anteriores')
            Registro.cor(f'A tabela não foi encontrada | Erro: {error}', 'vermelho')
            logging.error(f'{error} | Local:Registros anteriores. Início | Data {data} | Hora {hora}\n')
        
        

def menu():
    Registro.sub_titulo(f'Registros do dia {data_escolhida_global}')
    print('''
(1) Listar Clientes
(2) Listar Valores             
(3) Voltar          
                            ''')
      

def escolher_opcao():
    while ciclo_ativo:
        menu()
        try:  
            opcao = int(input('Seleciona uma opção acima. de 1 a 3: '))
        
            if 1 < opcao > 4:
                menu()
                Registro.cor('Entrada inválida. Digite uma opção de 1 a 3', 'vermelho')
            
            if opcao == 1:
                Registro.sub_titulo('Lista de clientes')
                cabecalho = (f'{"Nome do cliente":<50} {"Forma de pagamento":<25} {"Mensalidade":<20} {"Notas"}')
                print(cabecalho)
                print('-' * 135)
                
                registros = cursor.execute(f'SELECT * FROM "{data_escolhida_global}" ORDER BY NOME').fetchall()
                if registros == []:
                    print(f'{"-":<50} {"-":^18} {" " * 6} {"-":<20} {"-"}')
                
                else:
                    for cliente in registros:

                        if cliente[4] is None:
                            print(f'{cliente[1]:<50} {cliente[2]:^18} {" " * 6} {cliente[3]:<20.2f} -'.replace('.',','))
                        else:
                            print(f'{cliente[1]:<50} {cliente[2]:^18} {" " * 6} {cliente[3]:<20.2f} {cliente[4]}'.replace('.',','))
                
                input('\nPressione ENTER para voltar.')
                menu()
            
            if opcao == 2:
                Registro.sub_titulo('Lista de Valores')

                valor_dinheiro = cursor.execute(f'SELECT SUM (MENSALIDADE) FROM "{data_escolhida_global}" WHERE FORMA_DE_PAGAMENTO = "Dinheiro"').fetchone()
                valor_disponivel = cursor.execute(f'SELECT SUM (TOTAL_RETIRADO) FROM "valor_{data_escolhida_global}" ').fetchone()


                if valor_dinheiro[0] is None or valor_disponivel[0] is None:
                    print('Total Dinheiro: R$ -')
                    
                else:
                    print(f'Total Dinheiro: R${valor_dinheiro[0] - valor_disponivel[0]:.2f}'.replace('.',','))

                valor_pix = cursor.execute(f'SELECT SUM (MENSALIDADE) FROM "{data_escolhida_global}" WHERE FORMA_DE_PAGAMENTO = "Pix"').fetchone()
                
                if valor_pix[0] is None or 0:
                    print('Total Pix: R$ -')

                else:
                    print(f'Total Pix: R${valor_pix[0]:.2f}'.replace('.',','))

                valor_deposito = cursor.execute(f'SELECT SUM (MENSALIDADE) FROM "{data_escolhida_global}" WHERE FORMA_DE_PAGAMENTO = "Depósito"').fetchone()
            
                if valor_deposito[0] is None or 0:
                    print('Total Depósito: R$ -')

                else:
                    print(f'Total Depósito: R${valor_deposito[0]:.2f}'.replace('.',','))
                
                total_retirado = cursor.execute(f'SELECT SUM (TOTAL_RETIRADO) FROM "valor_{data_escolhida_global}"').fetchone()
                
                if total_retirado[0] is None or total_retirado[0] == 0:
                    Registro.cor('Total Retirado: R$ -','vermelho')
                else:
                    for valor in total_retirado:

                        Registro.cor(f'Total Retirado: R${valor:.2f}'.replace('.',','), 'vermelho')

                valor_total = cursor.execute(f'SELECT SUM (MENSALIDADE) FROM "{data_escolhida_global}"').fetchone()
                
                if valor_total[0] is None or valor_disponivel[0] is None:
                    Registro.cor('\nValor Total: R$ -', 'verde')
                else:
                    total = valor_total[0] - valor_disponivel[0]
                    Registro.cor(f'\nValor Total: R${total:.2f}'.replace('.',','), 'verde')


                print('\n')

                print(f'{"Saída":<10}        {"Notas":<50}')
                print('-' * 100)
                
                saidas = cursor.execute(f'SELECT * FROM "valor_{data_escolhida_global}" LIMIT -1 OFFSET 1').fetchall()

                if saidas == []:
                    print(f'{"-":<10}   {"-":<50}')

                else:
                    for saida in saidas:
                        #print(saida)
                        print(f'R${saida[2]:<10.2f}      {saida[3]:<50}'.replace('.',','))                        
                
                input('\nPresione ENTER para voltar')
                menu()

            if opcao == 3:
                registro_anterior()

        except Exception as error:
            menu()
            Registro.cor('Entrada inválida. Digite uma opção de 1 a 3', 'vermelho')
            logging.error(f'{error} | Local:Menu de opções. inicio | Data {data} | Hora {hora}\n')

    
def inicio():
    menu()
    escolher_opcao()

def main2():
    registro_anterior()
    escolher_opcao()
