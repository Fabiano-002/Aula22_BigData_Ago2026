import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


subprocess.run('cls', shell=True)
# Obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    
    df_cvli = df_ocorrencias[['aisp','cvli']]

    df_cvli= df_cvli.groupby('aisp', as_index=False)['cvli'].sum()
    df_cvli = df_cvli.sort_values(
        by='aisp',
        ascending=False
    )

    print(df_cvli)

except Exception as e:
    print(f'Erro ao obter os dados - {e}')

try:
    array_cvli = np.array(df_cvli['cvli'])
    media_cvli = np.mean(array_cvli)
    mediana_cvli = np.median(array_cvli)
    distancia = abs(
        (media_cvli - mediana_cvli) / mediana_cvli * 100
    )

    print('\nMedida de Tendência Central')
    print(f'Média: {(media_cvli)}')
    print(f'Mediana: {(mediana_cvli)}')
    print(f'Distância entre média e mediana: {distancia:.2f}%')

except Exception as e:
    print(f'Erro ao obter os dados - {e}')  

try:

    q1= np.quantile(array_cvli, .25)
    q2= np.quantile(array_cvli, .50)
    q3= np.quantile(array_cvli, .75) 

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    df_cvli_menores = df_cvli [
        df_cvli['cvli'] < q1
    ]

    df_cvli_maiores = df_cvli [
        df_cvli['cvli'] > q3 
    ]
    # Menores
    print('\nMunicípios com menores cvli')
    print(30*'-')
    print(df_cvli_menores.sort_values(by='cvli', ascending=True))
    df_cvli_menores.to_csv('menores.csv', index=False, sep=';',encoding='iso-8859-1' )

    # Maiores
    print('\nMunicípios com maiores cvli')
    print(30*'-')
    print(df_cvli_maiores.sort_values(by='cvli', ascending=True))
    df_cvli_maiores.to_csv('maiores.csv', index=False, sep=';',encoding='iso-8859-1')

except Exception as e:
    print(f'Erro ao analisar as distribuição {e}')

try:
    print('\nCalculando a Amplitude Total')

    maximo = np.max(array_cvli)
    minimo = np.min(array_cvli)
    amplitude = maximo - minimo

except Exception as e:    
    print(f'Erro ao calcular a amplitude {e}')

try:

    variancia = np.var(array_cvli)
    distancia_var_media= variancia / (media_cvli ** 2) *100
    desvio_padrao = np.std(array_cvli)
    coef_variacao = (desvio_padrao/media_cvli) * 100

except Exception as e:
    print(f'Erro ao calcular a variabilidade do conjunto: {e}')

try:
    assimetria = df_cvli['cvli'].skew()

    curtose = df_cvli['cvli'].kurtosis()
    
except Exception as e:
    print(f'Erro ao calcular a Assimetria e Curtose dos Dados: {e}')    