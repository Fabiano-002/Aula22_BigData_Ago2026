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

    print('\nAnalisando a Distribuição')
    print(30*'-')
    print(f'Assimetria: {assimetria:.2f}')
    print(f'Curtose: {curtose:.2f}')


except Exception as e:
    print(f'Erro ao calcular a Assimetria e Curtose dos Dados: {e}')

    # Achando os outliers
    
try:

    # Intervalor Interquartil : (IQR) 


    iqr = q3 - q1
    print(iqr) 


    limite_superior = q3 + 1.5 * iqr
    limite_inferior = q1 - 1.5 * iqr

    print(f'Limite Superior: {limite_superior}')
    print(f'Limite Inferior: {limite_inferior}')

    df_cvli_outliers_menores =(
        df_cvli[df_cvli['cvli'] < limite_inferior]
    )
    print('\nMunicípios com outliers inferiores')
    print(30*'-')
    if len(df_cvli_outliers_menores) == 0:
        print('Não há outliers inferiores')
    else:
        print(df_cvli_outliers_menores)


    df_cvli_outliers_maiores =(
        df_cvli[df_cvli['cvli'] > limite_superior]

    )  
    print('\nMunicípios com outliers superiores')
    print(30*'-')
    if len(df_cvli_outliers_maiores) == 0:
        print('Não há outliers superiores')
    else:
        print(df_cvli_outliers_maiores)

except Exception as e:
    print(f'Erro ao calcular os outliers: {e}')

try:
    print('\nMostrando Medidas')
    print(30*'-')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior:{limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')
    print(f'Total de cvli: {total_cvli}')

    print(f'Média: {media_cvli:.2f}')
    print(f'Mediana: {mediana_cvli:.2f}')
    print(f'Distância: {distancia:.2f}%')
    print(f'IQR: {iqr}')
    print(f'Amplitude: {amplitude}')
    print(f'Variância: {variancia:.2f}')
    print(f'Distância Variância e Média: {distancia_var_media:.2f}%')
    print(f'Desvio Padrão: {desvio_padrao:.2f}')
    print(f'Coeficiente de Variação: {coef_variacao:.2f}%')

except Exception as e:
    print(f'\nErro ao mostrar as medidas: {e} ')

    # Plotando Gráfico

#try:
    #print('Plotando Boxplot')
    # pip install matplotlib
    # import matplotlib.pyplot as plt 

    # Boxplot
    #plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation= 'horizontal', showmeans= True)

    # plt.show()

# except Exception as e:
    # print (f'Erro ao plotar grafico: {e}')


try:
    print('\nInformações de cvli')
    plt.figure(figsize={12,10})

    # Posição 1 

    plt.subplot(2,2,1)

    plt.boxplot(df_cvli['cvli'], orientation='horizontal', showmeans=True)
    plt.title('Distribuição dos Dados')
    plt.xlabel('cvli')
    plt.ylabel('Municípios')      

    plt.subplot(2,2,2)  
    plt.text(0.1, 0.95 , f'Limite Inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.90 , f'Mínimo: {minimo}', fontsize=12) 
    plt.text(0.1, 0.85 , f'Q1:{q1}' , fontsize=12 )
    plt.text(0.1, 0.80 , f'Q2:{q2}' , fontsize=12 )
    plt.text(0.1, 0.75 , f'Q3:{q3}' , fontsize=12 )
    plt.text(0.1, 0.70 , f'Limite Superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.65 , f'Máximo: {maximo}', fontsize=12)

    plt.text(0.1, 0.55, f'Mediana: {mediana_cvli}', fontsize=12 )
    plt.text(0.1, 0.50, f'Média: {media_cvli}',fontsize=12  )
    plt.text(0.1, 0.45, f'IQR Intervalo Interquartil: {iqr}',fontsize=12 )
    plt.text(0.1, 0.40, f'Amplitude Total: {amplitude}',fontsize=12  )
    plt.text(0.1, 0.35, f'Distância Total: {distancia}', fontsize=12 )
    plt.axis('off')

    plt.subplot(2, 2 ,3)

    plt.hist(array_cvli, bins=100, edgecolor='black') 
    plt.axvline(media_cvli, color ='green', linewidth=1) # Média
    plt.axvline(mediana_cvli, color ='orange', linewidth=1) # Mediana

    contagens, limites = np.histogram(array_cvli, bins=100)

    print(f'\nFaixas de cvli do Histograma:')
    for i in range(len(contagens)):
        print(
            f'Faixa: {i+1}:'
            f'{limites[i]:.0f} até {limites[i+1]:.0f} cvli '
            f'=>{contagens[i]} Municípios'
        )
        plt.bar(df_cvli_10maiores['aisp'], df_cvli_10maiores['cvli'])
        plt.xlabel('Município')
        plt.ylabel('cvli')
        plt.xticks(rotation=45, ha='right') # Rotaciona
        
        plt.suptitle ('Informações de cvli')
        plt.show()

except Exception as e:
    print(f'Erro ao plotar o gráfico: {e}')
