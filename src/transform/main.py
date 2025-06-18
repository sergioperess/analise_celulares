# %%

# imports
import pandas as pd
from datetime import datetime
import sqlite3

# %%

# Definir o caminho para o arquivo JSON
df = pd.read_json('../../data/magalu.json')

# %%

# Adicionar a coluna _source com um valor fixo
df['_source'] = "https://www.magazineluiza.com.br/busca/iphone/"
# %%

# Adicionar a coluna _data_coleta com a data e hora atuais
df['_datetime'] = datetime.now()

# %%

# Mostrar quando valores nulos existem nem cada coluna
print("Valores nulos na coluna de preços antigos:", df['old_price'].isnull().sum())
print("Valores nulos na coluna de preços novos:", df['new_price'].isnull().sum())
print("Valores nulos na coluna de rating numbers:", df['reviews_rating_number'].isnull().sum())

# Tratar nulos
df['old_price'] = df['old_price'].fillna('0')
df['new_price'] = df['new_price'].fillna('0')
df['reviews_rating_number'] = df['reviews_rating_number'].fillna('0')

# %%

# Separar a coluna de rating em avg_rating e rating_amount
df[['avg_rating', 'rating_amount']] = df['reviews_rating_number'].str.extract(r'([\d.]+)\s*\((\d+)\)')

# Elimina os valores nulos 
df['rating_amount'] = df['rating_amount'].fillna('0')


# %%

# Garantir que estão como strings antes de usar .str
df['old_price'] = (df['old_price']
                   .astype(str).str.replace(r"R\$\xa0", "", regex=True) 
                   .str.replace(".", "", regex=False)        
                   .str.replace(",", ".", regex=False)
                   )

df['new_price'] = (df['new_price']
                   .astype(str).str.replace(r"R\$\xa0", "", regex=True) 
                   .str.replace(".", "", regex=False)        
                   .str.replace(",", ".", regex=False)
                   )

# %%

# Converter para números

df['old_price'] = df['old_price'].astype(float)
df['new_price'] = df['new_price'].astype(float)
df['avg_rating'] = df['avg_rating'].astype(float)
df['rating_amount'] = df['rating_amount'].astype(int)

# %%

# Manter apenas produtos com preço maiores que 2000 
# Evita outros tipos de produtos como capinhas e peliculas

df = df[
    (df['old_price'] >= 2000) &
    (df['new_price'] >= 2000)
]

# %%
# Conectar ao banco de dados SQLite (ou criar um novo)
conn = sqlite3.connect('../../data/celulares.db')

# Salvar o DataFrame no banco de dados SQLite
df.to_sql('magalu', conn, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
conn.close()

# %%
