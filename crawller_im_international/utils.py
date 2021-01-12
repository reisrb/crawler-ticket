import csv
from typing import List
from datetime import date

def write_csv(matrix: List[List[str]]):
  today = date.today().strftime('%Y-%m-%d')

  header = ['TIPO', 'DATA_CONSULTA', 'ORIGEM', 'DESTINO', 'DATA_IDA', 'DATA_VOLTA', 'AGENCIA','COMPANHIA_IDA', 'DIRETO', 'UMA_PARADA', 'DUAS_OU_MAIS_PARADAS', 'AEROPORTO_EMBARQUE_IDA', 'HORA_EMBARQUE_IDA', 'AEROPORTO_DESEMBARQUE_IDA', 'HORA_DESEMBARQUE_IDA', 'DIAS_VIAGEM_IDA', 'DURACAO_VIAGEM_IDA', 'TIPO_VIAGEM_IDA', 'MOCHILA_IDA', 'BAGAGEM_MAO_IDA', 'MALA_IDA', 'COMPANHIA_VOLTA','AEROPORTO_EMBARQUE_VOLTA', 'HORA_EMBARQUE_VOLTA', 'AEROPORTO_DESEMBARQUE_VOLTA', 'HORA_DESEMBARQUE_VOLTA', 'DIAS_VIAGEM_VOLTA', 'DURACAO_VIAGEM_VOLTA', 'TIPO_VIAGEM_VOLTA', 'MOCHILA_VOLTA', 'BAGAGEM_MAO_VOLTA', 'MALA_VOLTA', 'PRECO_TOTAL']

  with open(f'../decolar_{today}.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)

    for list in matrix:
      for row in list:
        writer.writerow(row)

def keep_trying(func: callable) -> str:
  retry_count = 2
  def wrapper(*args):
    for tryies in range(retry_count):
      try:
        return func(*args)
      except Exception as e:
        print(e)
        print(f'Trying for the {tryies}th time...')
    return ' '
  return wrapper