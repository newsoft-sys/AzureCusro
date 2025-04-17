import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import uuid
import json
import pyodbc
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter informações de conexão do banco de dados
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USER")
password = os.getenv("SQL_PASSWORD")

# Verificar se as variáveis de ambiente foram carregadas corretamente
if not server or not database or not username or not password:
    print("Erro: Uma ou mais variáveis de ambiente não foram carregadas corretamente.")
    print(f"SQL_SERVER: {server}")
    print(f"SQL_DATABASE: {database}")
    print(f"SQL_USER: {username}")
    print(f"SQL_PASSWORD: {'***' if password else None}")
    exit(1)

# Atualizar a string de conexão para usar o Driver 18 e o formato correto do servidor
connection_string = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER=tcp:{server},1433;"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

# Restaurar o uso do Azure Blob Storage para salvar imagens
blob_service_client = BlobServiceClient.from_connection_string(os.getenv("BLOB_CONNECTION_STRING"))
blob_container_name = os.getenv("BLOB_CONTAINER_NAME")

st.title("Cadastro de Produtos")
produto = st.text_input("Nome do Produto")
preco = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")       
descricao = st.text_area("Descrição do Produto")
quantidade = st.number_input("Quantidade em Estoque", min_value=0, format="%d") 
imagem = st.file_uploader("Carregar Imagem do Produto", type=["jpg", "jpeg", "png"])

# Definir a variável botao_cadastrar antes de usá-la
botao_cadastrar = st.button("Cadastrar Produto")

# Ajustar o código para salvar apenas no banco de dados
if botao_cadastrar:
    if produto and preco and descricao and quantidade:
        # Ajustar o código para fazer upload da imagem para o contêiner
        if imagem:
            blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=imagem.name)
            blob_client.upload_blob(imagem, overwrite=True)
            imagem_url = f"https://{os.getenv('BLOB_ACCOUNT_NAME')}.blob.core.windows.net/{blob_container_name}/{imagem.name}"
        else:
            imagem_url = None

        try:
            # Conectar ao banco de dados e inserir o produto
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            # Ajustar a consulta SQL para salvar a URL da imagem no banco de dados
            cursor.execute(
                "INSERT INTO produtos (nome, preco, descricao, quantidade, imagem_url) VALUES (?, ?, ?, ?, ?)",
                (produto, preco, descricao, quantidade, imagem_url)
            )
            connection.commit()
            cursor.close()
            connection.close()
            st.success("Produto cadastrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao cadastrar o produto: {e}")

     

# Exibir produtos cadastrados   
st.subheader("Produtos Cadastrados")    
# Conectar ao banco de dados e buscar os produtos cadastrados
try:
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    # Atualizar a consulta SQL para incluir a coluna de imagem
    cursor.execute("SELECT id, nome, preco, descricao, quantidade, imagem_url FROM produtos")
    produtos = cursor.fetchall()
    cursor.close()
    connection.close()

    # Adicionar verificação para tratar casos em que a imagem seja None
    if produtos:
        cols = st.columns(4)  # Criar 4 colunas para exibir os cards
        for index, produto in enumerate(produtos):
            with cols[index % 4]:  # Alternar entre as colunas
                imagem_url = produto[5] if produto[5] else "https://via.placeholder.com/150"  # Usar imagem padrão se None
                st.image(imagem_url, use_container_width=True)  # Exibir a imagem
                st.markdown(f"**ID:** {produto[0]}")
                st.markdown(f"**Nome:** {produto[1]}")
                st.markdown(f"**Preço:** R$ {produto[2]:.2f}")
                st.markdown(f"**Descrição:** {produto[3]}")
                st.markdown(f"**Quantidade:** {produto[4]}")
    else:
        st.info("Nenhum produto cadastrado.")
except Exception as e:
    st.error(f"Erro ao buscar produtos cadastrados: {e}")       
# Exibir mensagem de erro se não houver conexão com o banco de dados
if not connection:
    st.error("Erro ao conectar ao banco de dados. Verifique as credenciais e a conexão.")
