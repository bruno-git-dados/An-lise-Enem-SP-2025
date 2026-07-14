import pandas as pd

# Definição de endpoints e diretórios de IO
arquivo_origem = 'RESULTADOS_2025.csv'
arquivo_destino = 'dados_enem_2025_SP.csv'

# Parâmetros de volumetria para processamento em lote (Batching)
chunk_size = 150000
primeiro_bloco = True

print("Iniciando a extração dos candidatos de SP direto da base de Resultados...")

# Pipeline de leitura segmentada para mitigação de estouro de memória RAM (Out-of-Core Processing)
for chunk in pd.read_csv(arquivo_origem, sep=';', encoding='latin-1', chunksize=chunk_size, low_memory=False):

    # Sanitização dos metadados das colunas (remoção de caracteres de escape e espaços residuais)
    chunk.columns = chunk.columns.str.strip()

    # Aplicação de filtro booleano focado no escopo geográfico da análise (UFs)
    chunk_sp = chunk[chunk['SG_UF_PROVA'] == 'SP']

    # Gerenciamento de persistência de dados em disco (I/O)
    if not chunk_sp.empty:
        if primeiro_bloco:
            # Inicialização do arquivo destino com persistência de cabeçalho
            chunk_sp.to_csv(arquivo_destino, index=False, mode='w', encoding='utf-8')
            primeiro_bloco = False
        else:
            # Escrita incremental em modo Append para otimização de fluxo de memória
            chunk_sp.to_csv(arquivo_destino, index=False, mode='a', header=False, encoding='utf-8')

print("Concluído com sucesso! Seu arquivo 'dados_enem_2025_SP.csv' está pronto para uso.")
