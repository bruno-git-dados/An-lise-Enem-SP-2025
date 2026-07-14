import pandas as pd
import matplotlib.pyplot as plt

# Parâmetros de formatação do output para inspeção via CLI
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', None)

# Ingestão do dataset processado (escopo estadual)
df = pd.read_csv('dados_enem_2025_SP.csv')

# Extração dinâmica de colunas de notas (exclusão de notas parciais/competências)
provas = df.columns[df.columns.str.contains('NOTA') & (~df.columns.str.contains('COMP'))].tolist()



# ANÁLISE 1: DENSIDADE POPULACIONAL POR MUNICÍPIO (TOP 10)
fig1, ax1 = plt.subplots(figsize=(10, 6))
(df['NO_MUNICIPIO_PROVA']
 .value_counts()
 .nlargest(10)
 .plot(kind='barh', color='blue', ax=ax1))

ax1.set_title('Top 10 Municípios Paulistas com Maior Quantidade de Inscritos no ENEM 2025')
ax1.set_xlabel('Quantidade de Candidatos')
ax1.set_ylabel('Município')



# ANÁLISE 2: DISTRIBUIÇÃO E MÉTRICAS DA PROVA DE REDAÇÃO
# Avaliação de dispersão e assimetria das notas
fig2, ax2 = plt.subplots(figsize=(10, 6))
df['NU_NOTA_REDACAO'].plot(kind='hist', bins=20, color='teal', edgecolor='black', ax=ax2)

ax2.set_title('Distribuição e Frequência das Notas de Redação em SP (ENEM 2025)')
ax2.set_xlabel('Nota da Redação')
ax2.set_ylabel('Frequência (Quantidade de Alunos)')

# Tratamento de outliers: isolamento de registros ausentes e notas zero (desistências/desclassificações)
mask1 = df.NU_NOTA_REDACAO.notna()
mask2 = df.NU_NOTA_REDACAO != 0
subset_redacao = df[(mask1) & (mask2)]

# Sumário descritivo e medidas de tendência central
print("=== ANÁLISE ESTATÍSTICA DAS NOTAS DE REDAÇÃO (EXCLUINDO ZERADAS) ===")
print(subset_redacao.NU_NOTA_REDACAO.agg(['min', 'mean', 'median', 'max']).round(2))
print("===================================================================\n")



# ANÁLISE 3: PERFORMANCE EDUCACIONAL POR LOCALIDADE (TOP 10)
# Engenharia de atributos: cálculo do score geral ponderado por linha (eixo horizontal)
df['NOTA_GERAL'] = df[provas].mean(axis=1)

# Filtro de significância estatística para mitigar distorções causadas por baixa amostragem
municipios_relevantes = df['NO_MUNICIPIO_PROVA'].value_counts()
municipios_filtrados = municipios_relevantes[municipios_relevantes > 100].index

# Agrupamento e extração dos maiores scores médios municipais
fig3, ax3 = plt.subplots(figsize=(10, 6))
(df[df['NO_MUNICIPIO_PROVA'].isin(municipios_filtrados)]
 .groupby('NO_MUNICIPIO_PROVA')['NOTA_GERAL']
 .mean()
 .nlargest(10)
 .plot(kind='bar', color='darkorange', edgecolor='black', ax=ax3))

# Renderização de data labels sobre o topo das estruturas
for container in ax3.containers:
    ax3.bar_label(container, fmt='%.1f', padding=3, fontsize=9)

ax3.set_title('Top 10 Municípios de SP com as Maiores Médias no ENEM 2025')
ax3.set_xlabel('Município')
ax3.set_ylabel('Média da Nota Geral')
plt.xticks(rotation=45, ha='right')

# Console output para auditoria do ranking ponderado
print("=== TOP 10 MUNICÍPIOS DE SP COM AS MAIORES MÉDIAS NO ENEM 2025 ===")
print(df[df['NO_MUNICIPIO_PROVA'].isin(municipios_filtrados)].groupby('NO_MUNICIPIO_PROVA')['NOTA_GERAL'].mean().nlargest(10).round(2))
print("=================================================================\n")



# PROCESSAMENTO DE RENDERIZAÇÃO INTERNA
plt.tight_layout()
plt.show()
