import pandas as pd
import matplotlib.pyplot as plt
import os 


pd.set_option('display.max_columns', None)  # Mostrar todas as colunas

# Criar pasta de gráficos
os.makedirs('graficos', exist_ok=True) 
os.makedirs('relatorios', exist_ok=True)

# LEITURA 
df_dados = pd.read_csv(
    'dados/V_OCORRENCIA_AMPLA.csv',
    sep=';',
    encoding='utf-8',
    low_memory=False,
    skiprows=1
)


# Remover colunas e linhas totalmente vazias
df_dados = df_dados.dropna(axis=1, how='all')
df_dados = df_dados.dropna(how='all')


# VISUALIZAÇÃO 
print("\nPrimeiras linhas:")
print(df_dados.head())

print("\nColunas do dataset:\n")

for i, coluna in enumerate(df_dados.columns, start=1):
    print(f"{i} - {coluna}")

# ANÁLISE DOS DADOS
print("\nOcorrências por estado:")
print(df_dados['UF'].value_counts())

print("\nTipos de ocorrência:")
print(df_dados['Classificacao_da_Ocorrencia'].value_counts())

# TRATAMENTO DAS FATALIDADES
df_dados['Lesoes_Fatais_Tripulantes'] = pd.to_numeric(
    df_dados['Lesoes_Fatais_Tripulantes'],
    errors='coerce'
).fillna(0)

df_dados['Lesoes_Fatais_Passageiros'] = pd.to_numeric(
    df_dados['Lesoes_Fatais_Passageiros'],
    errors='coerce'
).fillna(0)

# Soma das fatalidades
df_dados['Total_Fatalidades'] = (
    df_dados['Lesoes_Fatais_Tripulantes'] +
    df_dados['Lesoes_Fatais_Passageiros']
)


# FATALIDADES POR ESTADO
fatalidades_estado = df_dados.groupby('UF')[
    'Total_Fatalidades'
].sum().sort_values(ascending=False)

print("\nTop 10 estados com mais fatalidades:")
print(fatalidades_estado.head(10))


# GRÁFICO DE FATALIDADES

# Selecionando o Top 10 para o gráfico
top_10_fatalidades = fatalidades_estado.head(10)

plt.figure(figsize=(12, 6))
bars = plt.barh(top_10_fatalidades.index[::-1], top_10_fatalidades.values[::-1], color='skyblue')

# Adicionar títulos e rótulos
plt.title('Top 10 Estados com Mais Fatalidades em Ocorrências Aeronáuticas', fontsize=14, pad=20)
plt.xlabel('Total de Fatalidades', fontsize=12)
plt.ylabel('Estado (UF)', fontsize=12)

for bar in bars:
    plt.text(
        bar.get_width() + 0.5, 
        bar.get_y() + bar.get_height()/2, 
        f'{int(bar.get_width())}', 
        va='center'
    )

plt.tight_layout() 

#Salvar
plt.savefig('graficos/fatalidades_estados.png') 

plt.show()


with open(
    'relatorios/relatorio.txt',
    'w',
    encoding='utf-8'
) as relatorio:

    relatorio.write('RELATÓRIO DE OCORRÊNCIAS AÉREAS\n')
    relatorio.write('=' * 40 + '\n\n')

    relatorio.write('TOP 10 ESTADOS COM MAIS OCORRÊNCIAS\n\n')

    relatorio.write(
        df_dados['UF']
        .value_counts()
        .head(10)
        .to_string()
    )

    relatorio.write('\n\n')

    relatorio.write('TOP 10 ESTADOS COM MAIS FATALIDADES\n\n')

    relatorio.write(
        fatalidades_estado
        .head(10)
        .to_string()
    )

print('\nRelatório salvo em relatorios/relatorio.txt')