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
   # utf-8, iso-8859-1, latin1, cp1252 

    # print(df_ocorrencias) 
    # Filtro 
    df_ocorrencias = df_ocorrencias[df_ocorrencias['regiao'] == 'Baixada Fluminense']

    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    # print(df_roubo_veiculo.head(30))
    # print(df_roubo_veiculo.tail(30))

    # PREPARANDO OS DADOS

    # Totalizando os Roubos por Cidade (Var Qualitativa 'munic' e Var Quant 'roubo_veiculo')
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()
    # print(df_roubo_veiculo)

    # Obtendo Percentual
    # Total
    total_roubos = df_roubo_veiculo['roubo_veiculo'].sum()

    # Percentual
    df_roubo_veiculo['percentual %'] = round(
        ((df_roubo_veiculo['roubo_veículo']) / total_roubos * 100), 2
    )

    # Ordenando os dados
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo',
        ascending=False

    )
    print(df_roubo_veiculo.head(10))
    # print(df_roubo_veiculo.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')

try:
    print(f'\nObtendo informações acerca dos roubos dos veículos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    #Distância da média para mediana 
    distancia = abs(
        (media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100
        )

    print('\nMedida de Tendência Central')
    print(f'Média: {(media_roubo_veiculo)}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância Média - Mediana:{distancia:.2f}%')


    
except Exception as e:
    print(f'Obtendo medidas - {e}')

try:

    q1 = np.quantile(array_roubo_veiculo, .25) # method='weibull'
    q2 = np.quantile(array_roubo_veiculo, .50) # method='weibull'
    q3 = np.quantile(array_roubo_veiculo, .75) # method='weibull'

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # Cidades com menores ocorrências de roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] < q1
    ]

    # Cidades com maiores ocorrências de roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] > q3
    ]
    # Menores
    print('\nMunicípios com menores roubos')
    print(30*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    df_roubo_veiculo_menores.to_csv('menores.csv', index=False, sep=';',encoding='iso-8859-1' )

    #Maiores
    print('\nMunicípios com maiores roubos')
    print(30*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=True))
    df_roubo_veiculo_maiores.to_csv('maiores.csv', index=False, sep=';',encoding='iso-8859-1')
    

except Exception as e:
    print(f'Erro ao analisar as distribuição {e}')

# Medidas de Posição e Dispersão  


try:
    print('\nCalculando a Amplitude Total')
    # Amplitude Total = maior valor - menor valor
    # Quanto mais próximo do 0, mais homogêneos são os dados do conjunto.
    # Quanto mais próximo do maior valor, mais heterogêneo são os dados do conjunto.
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

except Exception as e:    
    print(f'Erro ao calcular a amplitude {e}')

# Medidas de Dispersão
try:
    # Variância
    # É uma medida p/ observar a dispersão dos dados.
    # Observa-se em relação a média.
    # É a média dos quadrados das diferenças entre cada valor e a média.
    # OBS: O resultado da variância está elevado ao Quadrado
    variancia = np.var(array_roubo_veiculo)

    # distância variâncie media
    # < 10% - Baixa Dispersão
    # Entre 10% e 25% - Tendência de Moderada Dispersão 
    # > 25% Alta Dispersão  
    distancia_var_media= variancia / (media_roubo_veiculo ** 2) * 100

    # Desvio Padrão 
    # É a raiz quadrada da Variância . Observa-se em relação a média.
    # É a normalização da variância.
    # Quantos os dados se afastam da Média

    desvio_padrao = np.std(array_roubo_veiculo)

    # Coeficiente de Variação 
    # É a magnitude do Desvio Padrão em relação a média
    coef_variacao = (desvio_padrao/ media_roubo_veiculo) * 100


except Exception as e:
    print(f'Erro ao calcular a variabilidade do conjunto: {e}')    

# Verificando a Assimetria da Distribuição
# Indica como os dados estão distribuidos.Para que lado tende a nossa distribuição.
try:

    # Assimetria > 1 
    # Positiva Alta
    # Cauda longa à direita 
    # Existem valores altos puxando essa média para cima
    # A média tende a ser maior que a mediana

    # Assimetria entre 0.5 e 1 
    # Assimetria Positiva Moderada
    # Existem valores altos puxando essa média para cima
    # A média tende a ser maior que a mediana

    # Assimetria entre -0.5 e 0.5 (Tendência Simetria)
    # Temdência a uma simetria
    # O dados tende a estar equilibrados em torno do centro    
    # A média e mediana tende a ter valores aproximados

    # Assimetria entre 0.5 e 1 
    # Assimetria Negativa Moderada
    # Cauda existe , mas menos acentuada 
    # A média tende a ser menor que a mediana


    # Assimetria < -1 
    # Assimetria negativa alta
    # Cauda longa à esquerda
    # A média tende a ser menor que a mediana
    # Existem valores baixos puxando a média para baixo

    assimetria = df_roubo_veiculo['roubo_veiculo'].skew()


    # Curtose
    # É uma medida que verifica  o peso das caudas de uma distribuição
    # Indicando a importância dos valores extremos.
    # Quanto maior a Curtose, maior tende a ser a influência dos extremos.

    # Referência: Excesso de Curtose de Fisher

    # -0.5 a 0.5 (Aproximadamente Mesocúrtica)
    # Curtose próxima de uma distribuição normal.
    # Outliers não são comuns, mas pode ocorrer.

    # Curtose > que 0.5 (Leptocúrtica)
    # Caudas mais longas e pesadas e maior influência dos extremos 
    # Poucos valores muito extremos elevando bastante a Curtose.
    # Pode apresentar picos muito altos
    # Outliers são mais frequentes

    # Curtose < -0.5 (Platcúrtica)
    # Caudas mais leves
    # Menor influência dos extremos.
    # Tende a Distribuição mais achatada.
    # Outlier podem a aparecer

    curtose = df_roubo_veiculo['roubo_veiculo'].kurtosis()


    print('\nAnalisando a Distribuição')
    print(30*'-')
    print(f'Assimetria: {assimetria:.2f}')
    print(f'Curtose: {curtose:.2f}')

except Exception as e:
    print(f'Erro ao calcular a Assimetria e Curtose dos Dados: {e}')   

# Achando os Outliers

try:
    #Intervalo Interquartil:  (IQR)  
    # É amplitude dos dados mais centrais
    # Ignora o maior e menor valor 
    # Não sofre interferência dos extremos 
    # Quanto mais próximo do 0, mais homogêneos são os dados mais centrais
    # Quanto mais próximo do Q3, mais heterogêneo são os dadosdos 50% mais centrais
    # 970.75

    iqr = q3 - q1
    print(iqr)

    # Calculando os limites
    # Superior 
    limite_superior = q3 + (1.5 * iqr)
    
    # Inferior
    limite_inferior = q1 - (1.5 * iqr)

    print(f'\nlimite_Superior: {limite_superior}')
    print(f'\nlimite_Inferior:{limite_inferior}')

    # Filtrando os Outliers menores

    df_roubo_veiculo_outliers_menores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo']< limite_inferior]

    )

    print('\nMunicípios com outliers inferiores')
    print(30*'-')      
    if len(df_roubo_veiculo_outliers_menores) == 0:
        print('Não há  outliers Inferiores')
    else:
        print(df_roubo_veiculo_outliers_menores)  

    # Filtrando os outliers maiores

    df_roubo_veiculo_outliers_maiores = (
            df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    
        )  
    print('\nMunicípios com outliers Superiores')
    print(30*'-')      
    if len(df_roubo_veiculo_outliers_maiores) == 0:
             print('Não há  outliers Superiores')
    else:
         print(df_roubo_veiculo_outliers_maiores)  

except Exception as e:
    print(f'Erro ao calcular os outliers {e}')   

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
    print(f'Total de Roubos: {total_roubos}')

    print(f'Média: {media_roubo_veiculo:.2f}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância: {distancia:.2f}%')
    print(f'IQR: {iqr}')
    print(f'Amplitude: {amplitude}')
    print(f'Variância: {variancia:.2f}')
    print(f'Distância Variância e Média: {distancia_var_media:.2f}%')
    print(f'Desvio Padrão: {desvio_padrao:.2f}')
    print(f'Coeficiente de Variação: {coef_variacao:.2f}%')
   

except Exception as e:
    print(f'\nErro aos mostrar medidas {e}')




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
    print('\nInformações de Roubos de Veículos')
    plt.figure(figsize={9,21})
    # Posição 1 Boxplot

    plt.subplot(2, 2, 1)
    
    # Boxplot - Definição : Serve para visualizar uma distribuição.
    # showmeans = mostra a média e showfliers = remove os outliers
    plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation='horizontal',showmeans=True)
    plt.title('Distribuição dos Dados')
    plt.xlabel('Roubo de Veículos')
    plt.ylabel('Municípios')

    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.95 , f'Limite Inferior: {limite_inferior}', fontsize=12 )
    plt.text(0.1, 0.90 , f'Mínimo: {minimo}',fontsize=12  )
    plt.text(0.1, 0.85 , f'Q1:{q1}' , fontsize=12 )
    plt.text(0.1, 0.80 , f'Q2:{q2}' , fontsize=12 )
    plt.text(0.1, 0.75 , f'Q3:{q3}' ,fontsize=12  )
    plt.text(0.1, 0.70 , f'Limite Superior: {limite_superior}',fontsize=12  )
    plt.text(0.1, 0.65 , f'Máximo: {maximo}', fontsize=12  )

    plt.text(0.1, 0.55, f'Mediana: {mediana_roubo_veiculo}', fontsize=12 )
    plt.text(0.1, 0.50, f'Média: {media_roubo_veiculo}',fontsize=12  )
    plt.text(0.1, 0.45, f'IQR Intervalo Interquartil: {iqr}',fontsize=12 )
    plt.text(0.1, 0.40, f'Amplitude Total: {amplitude}',fontsize=12  )
    plt.text(0.1, 0.35, f'Distância Total: {distancia}', fontsize=12 )
    plt.axis('off')

    # Histograma | Roubos por Município
    plt.subplot(2, 2, 3)
    # Histograma
    plt.hist(array_roubo_veiculo, bins=100, edgecolor='black')
    plt.axvline(media_roubo_veiculo, color = 'green', linewidth=1) # média
    plt.axvline(mediana_roubo_veiculo, color = 'orange', linewidth=1) # mediana


    contagens, limites = np.histogram(array_roubo_veiculo, bins=100)


    print(f'\nFaixas de Roubos do Histograma')
    for i in range(len(contagens)):
        if contagens[i] > 0:
            print(
                f'Faixa {i+1}:'
                f'{limites[i]:.0f} até {limites[i+1]:.0f} Roubos '
                f'=> {contagens[i]} Municípios'
        )


    # 4ª Posição -Colunas | Top 10 Maiores 
    plt.subplot(2, 2, 4)

    df_roubo_veiculo_10maiores = (
        df_roubo_veiculo_maiores
        .head(10)
        .sort_values(by='roubo_veiculo', ascending=True)
    )

    plt.bar(df_roubo_veiculo_10maiores['munic'], df_roubo_veiculo_10maiores['roubo_veiculo'])
    plt.xlabel('Município')
    plt.ylabel('Roubo de Veículos')
    plt.xticks(rotation=45, ha='right') # Rotaciona

    plt.suptitle('Informações sobre Roubo de Veículos')
    plt.show()

except Exception as e:
    print (f'Erro ao plotar grafico: - {e}')    