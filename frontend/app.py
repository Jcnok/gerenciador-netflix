import streamlit as st
import requests
import json

st.set_page_config(page_title="Gerenciador Netflix", page_icon="🎬")

st.title("🎬 Gerenciador de Catálogos Netflix")

# Configurações das Azure Functions (devem ser configuradas)
BASE_URL = st.secrets.get("FUNCTION_BASE_URL", "https://func-netflix-catalog.azurewebsites.net/api")

tabs = st.tabs(["📤 Upload", "💾 Salvar", "📋 Listar", "🔍 Buscar"])

# Tab 1: Upload de Arquivo
with tabs[0]:
    st.header("Upload de Catálogo")
    uploaded_file = st.file_uploader("Escolha um arquivo", type=['csv', 'json', 'txt'])
    filename = st.text_input("Nome do arquivo")
    
    if st.button("Enviar Arquivo"):
        if uploaded_file and filename:
            try:
                response = requests.post(
                    f"{BASE_URL}/upload_file?filename={filename}",
                    data=uploaded_file.getvalue()
                )
                if response.status_code == 200:
                    st.success("Arquivo enviado com sucesso!")
                else:
                    st.error(f"Erro: {response.json()}")
            except Exception as e:
                st.error(f"Erro ao enviar: {str(e)}")

# Tab 2: Salvar Catálogo
with tabs[1]:
    st.header("Salvar Novo Catálogo")
    catalog_id = st.text_input("ID do Catálogo")
    catalog_name = st.text_input("Nome")
    catalog_desc = st.text_area("Descrição")
    
    if st.button("Salvar Catálogo"):
        if catalog_id and catalog_name:
            try:
                data = {
                    "id": catalog_id,
                    "name": catalog_name,
                    "description": catalog_desc
                }
                response = requests.post(f"{BASE_URL}/salvar_catalogo", json=data)
                if response.status_code == 201:
                    st.success("Catálogo salvo com sucesso!")
                else:
                    st.error(f"Erro: {response.json()}")
            except Exception as e:
                st.error(f"Erro ao salvar: {str(e)}")

# Tab 3: Listar Catálogos
with tabs[2]:
    st.header("Catálogos Disponíveis")
    
    if st.button("Carregar Catálogos"):
        try:
            response = requests.get(f"{BASE_URL}/listar_catalogos")
            if response.status_code == 200:
                catalogs = response.json().get('catalogs', [])
                if catalogs:
                    for catalog in catalogs:
                        with st.expander(f"📁 {catalog.get('name', 'Sem nome')}"):
                            st.json(catalog)
                else:
                    st.info("Nenhum catálogo encontrado")
            else:
                st.error(f"Erro: {response.json()}")
        except Exception as e:
            st.error(f"Erro ao listar: {str(e)}")

# Tab 4: Buscar Catálogo
with tabs[3]:
    st.header("Buscar Catálogo")
    search_id = st.text_input("ID do Catálogo para buscar")
    
    if st.button("Buscar"):
        if search_id:
            try:
                response = requests.get(f"{BASE_URL}/buscar_catalogo?id={search_id}")
                if response.status_code == 200:
                    catalog = response.json().get('catalog', {})
                    st.success("Catálogo encontrado!")
                    st.json(catalog)
                else:
                    st.error(f"Erro: {response.json()}")
            except Exception as e:
                st.error(f"Erro ao buscar: {str(e)}")

st.markdown("---")
st.markdown("💡 **Dica:** Configure as URLs das Azure Functions em `.streamlit/secrets.toml`")
