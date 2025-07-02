# %%

# import
import streamlit as st
import pandas as pd
import sqlite3

# %%

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('data/celulares.db')

# %%

# Carregar os dados da tabela 'notebooks' em um DataFrame pandas
df = pd.read_sql_query("SELECT * FROM magalu", conn)
df.head()

# %%

# Fechar a conexão com o banco de dados
conn.close()
# %%

# Título
st.title('📱 Dashboard de Celulares - Magalu')
st.subheader('Análise de preços e avaliações dos produtos')

# ---------- Celular com menor preço ----------
min_price_row = df.loc[df['new_price'].idxmin()]
st.markdown("### 🔽 Celular com o menor preço:")

col1, col2 = st.columns([1, 3])
with col1:
    st.image(min_price_row['image'], width=150)
with col2:
    st.write(f"**Produto:** {min_price_row['name']}")
    st.write(f"**Preço:** R$ {min_price_row['new_price']:.2f}")
    st.write(f"**Nota média:** {min_price_row['avg_rating']:.2f}")
    st.write(f"**Quantidade de avaliações:** {min_price_row['rating_amount']}")

# ---------- Celular com maior preço ----------
max_price_row = df.loc[df['new_price'].idxmax()]
st.markdown("### 🔼 Celular com o maior preço:")

col1, col2 = st.columns([1, 3])
with col1:
    st.image(max_price_row['image'], width=150)
with col2:
    st.write(f"**Produto:** {max_price_row['name']}")
    st.write(f"**Preço:** R$ {max_price_row['new_price']:.2f}")
    st.write(f"**Nota média:** {max_price_row['avg_rating']:.2f}")
    st.write(f"**Quantidade de avaliações:** {max_price_row['rating_amount']}")

# ---------- Celular com maior número de avaliações ----------
most_rated_row = df.loc[df['rating_amount'].idxmax()]
st.markdown("### 🗳️ Celular com maior número de avaliações:")

col1, col2 = st.columns([1, 3])
with col1:
    st.image(most_rated_row['image'], width=150)
with col2:
    st.write(f"**Produto:** {most_rated_row['name']}")
    st.write(f"**Preço:** R$ {most_rated_row['new_price']:.2f}")
    st.write(f"**Nota média:** {most_rated_row['avg_rating']:.2f}")
    st.write(f"**Quantidade de avaliações:** {most_rated_row['rating_amount']}")


st.markdown("### 🍎 iPhone 16 ")

# Filtrar o DataFrame para encontrar o iPhone 16
iphone_16 = df[df['name'].str.contains("iphone 16 128", case=False, na=False)]

if not iphone_16.empty:
    produto = iphone_16.iloc[0]['name']
    preco = f"R$ {iphone_16.iloc[0]['new_price']:.2f}"
    rating = iphone_16.iloc[0].get('avg_rating', 'N/A')
    rating_count = iphone_16.iloc[0].get('rating_amount', 'N/A')
    imagem = iphone_16.iloc[0].get('image', '')

    col1, col2 = st.columns([1, 3])
    with col1:
        if imagem:
            st.image(imagem, width=150)
        else:
            st.write("📷 Sem imagem disponível")

    with col2:
        st.write(f"**Produto:** {produto}")
        st.write(f"**Preço:** {preco}")
        st.write(f"**Nota média:** {rating}")
        st.write(f"**Quantidade de avaliações:** {rating_count}")
else:
    
    st.warning("📦 Nenhum iPhone 16 128GB encontrado no banco de dados.")
# %%
# Rodapé
st.caption("Dados coletados da Magalu. Atualizado automaticamente via banco SQLite.")
