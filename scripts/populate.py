#!/usr/bin/env python3
"""
Script de população do catálogo Netflix

Este script faz upload de imagens e vídeos de exemplo para o Azure Storage
e popula o banco de dados CosmosDB através da API do Azure Functions.

Antes de executar:
1. Configure as variáveis de ambiente com as credenciais Azure
2. Baixe assets gratuitos de:
   - Vídeos: https://pixabay.com/videos/ ou https://www.pexels.com/videos/
   - Imagens: https://pixabay.com/images/ ou https://www.pexels.com/
3. Coloque os arquivos nas pastas: 
   - ./assets/videos/
   - ./assets/thumbnails/
"""

import os
import json
import requests
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
from pathlib import Path
import sys

# Configurações do Azure (variáveis de ambiente)
STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
COSMOSDB_ENDPOINT = os.getenv('COSMOSDB_ENDPOINT')
COSMOSDB_KEY = os.getenv('COSMOSDB_KEY')
COSMOSDB_DATABASE = os.getenv('COSMOSDB_DATABASE', 'NetflixDB')
COSMOSDB_CONTAINER = os.getenv('COSMOSDB_CONTAINER', 'movies')
FUNCTION_APP_URL = os.getenv('FUNCTION_APP_URL')

# Containers do Storage
THUMBNAILS_CONTAINER = 'thumbnails'
VIDEOS_CONTAINER = 'videos'

# Diretórios locais com os assets
ASSETS_DIR = Path('./assets')
VIDEOS_DIR = ASSETS_DIR / 'videos'
THUMBNAILS_DIR = ASSETS_DIR / 'thumbnails'

# Dados de exemplo para filmes
MOVIES_DATA = [
    {
        "id": "1",
        "title": "Aventura nas Montanhas",
        "description": "Uma jornada emocionante pelas montanhas mais altas do mundo.",
        "genre": "Aventura",
        "year": 2024,
        "duration": 120,
        "rating": 4.5
    },
    {
        "id": "2",
        "title": "Mistérios da Floresta",
        "description": "Descubra os segredos escondidos nas profundezas da floresta.",
        "genre": "Drama",
        "year": 2023,
        "duration": 105,
        "rating": 4.2
    },
    {
        "id": "3",
        "title": "Velocidade Máxima",
        "description": "Ação intensa com corridas de carros em alta velocidade.",
        "genre": "Ação",
        "year": 2024,
        "duration": 95,
        "rating": 4.7
    },
    {
        "id": "4",
        "title": "Romance no Litoral",
        "description": "Uma história de amor inesquecível à beira-mar.",
        "genre": "Romance",
        "year": 2023,
        "duration": 110,
        "rating": 4.3
    },
    {
        "id": "5",
        "title": "Comédia dos Erros",
        "description": "Risadas garantidas com situações hilarántes.",
        "genre": "Comédia",
        "year": 2024,
        "duration": 88,
        "rating": 4.0
    }
]

def check_environment():
    """Verifica se todas as variáveis de ambiente estão configuradas"""
    missing_vars = []
    
    if not STORAGE_CONNECTION_STRING:
        missing_vars.append('AZURE_STORAGE_CONNECTION_STRING')
    if not COSMOSDB_ENDPOINT:
        missing_vars.append('COSMOSDB_ENDPOINT')
    if not COSMOSDB_KEY:
        missing_vars.append('COSMOSDB_KEY')
    if not FUNCTION_APP_URL:
        missing_vars.append('FUNCTION_APP_URL')
    
    if missing_vars:
        print("\u274c Erro: Variáveis de ambiente não configuradas:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nConfigure-as usando:")
        print("   export AZURE_STORAGE_CONNECTION_STRING='...'")
        print("   export COSMOSDB_ENDPOINT='...'")
        print("   export COSMOSDB_KEY='...'")
        print("   export FUNCTION_APP_URL='...'")
        return False
    
    return True

def check_assets_directories():
    """Verifica se os diretórios de assets existem e contém arquivos"""
    if not ASSETS_DIR.exists():
        print(f"\u274c Erro: Diretório {ASSETS_DIR} não encontrado.")
        print("\nCrie a estrutura de diretórios e baixe assets gratuitos:")
        print("   mkdir -p assets/videos assets/thumbnails")
        print("\nBaixe vídeos gratuitos de:")
        print("   - https://pixabay.com/videos/")
        print("   - https://www.pexels.com/videos/")
        print("\nBaixe imagens gratuitas de:")
        print("   - https://pixabay.com/images/")
        print("   - https://www.pexels.com/")
        return False
    
    if not VIDEOS_DIR.exists() or not list(VIDEOS_DIR.glob('*')):
        print(f"\u274c Aviso: Nenhum vídeo encontrado em {VIDEOS_DIR}")
        print("   Baixe vídeos de exemplo e salve neste diretório.")
    
    if not THUMBNAILS_DIR.exists() or not list(THUMBNAILS_DIR.glob('*')):
        print(f"\u274c Aviso: Nenhuma imagem encontrada em {THUMBNAILS_DIR}")
        print("   Baixe imagens de exemplo e salve neste diretório.")
    
    return True

def upload_blob(blob_service_client, container_name, file_path, blob_name):
    """Faz upload de um arquivo para o Azure Blob Storage"""
    try:
        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name
        )
        
        with open(file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        print(f"  \u2713 Upload concluído: {blob_name}")
        return blob_client.url
    except Exception as e:
        print(f"  \u274c Erro no upload de {blob_name}: {str(e)}")
        return None

def upload_assets():
    """Faz upload de todos os assets para o Azure Storage"""
    print("\n📤 Iniciando upload de assets...")
    
    blob_service_client = BlobServiceClient.from_connection_string(
        STORAGE_CONNECTION_STRING
    )
    
    uploaded_files = {'videos': {}, 'thumbnails': {}}
    
    # Upload de vídeos
    print("\n🎥 Upload de vídeos:")
    if VIDEOS_DIR.exists():
        video_files = list(VIDEOS_DIR.glob('*'))
        for i, video_file in enumerate(video_files[:5], 1):  # Limita a 5 vídeos
            if video_file.is_file():
                blob_name = f"video_{i}{video_file.suffix}"
                url = upload_blob(
                    blob_service_client,
                    VIDEOS_CONTAINER,
                    video_file,
                    blob_name
                )
                if url:
                    uploaded_files['videos'][str(i)] = url
    
    # Upload de thumbnails
    print("\n🖼️ Upload de thumbnails:")
    if THUMBNAILS_DIR.exists():
        thumbnail_files = list(THUMBNAILS_DIR.glob('*'))
        for i, thumb_file in enumerate(thumbnail_files[:5], 1):  # Limita a 5 imagens
            if thumb_file.is_file():
                blob_name = f"thumbnail_{i}{thumb_file.suffix}"
                url = upload_blob(
                    blob_service_client,
                    THUMBNAILS_CONTAINER,
                    thumb_file,
                    blob_name
                )
                if url:
                    uploaded_files['thumbnails'][str(i)] = url
    
    return uploaded_files

def populate_database(uploaded_files):
    """Popula o banco de dados CosmosDB com os dados dos filmes"""
    print("\n💾 Populando banco de dados...")
    
    cosmos_client = CosmosClient(COSMOSDB_ENDPOINT, COSMOSDB_KEY)
    database = cosmos_client.get_database_client(COSMOSDB_DATABASE)
    container = database.get_container_client(COSMOSDB_CONTAINER)
    
    for movie in MOVIES_DATA:
        movie_id = movie['id']
        
        # Adiciona URLs dos assets se disponíveis
        if movie_id in uploaded_files['videos']:
            movie['videoUrl'] = uploaded_files['videos'][movie_id]
        
        if movie_id in uploaded_files['thumbnails']:
            movie['thumbnailUrl'] = uploaded_files['thumbnails'][movie_id]
        
        try:
            container.upsert_item(movie)
            print(f"  \u2713 Filme adicionado: {movie['title']}")
        except Exception as e:
            print(f"  \u274c Erro ao adicionar {movie['title']}: {str(e)}")

def main():
    print("🎬 Script de População do Catálogo Netflix")
    print("="*60)
    
    # Verifica configurações
    if not check_environment():
        sys.exit(1)
    
    check_assets_directories()
    
    # Pergunta se o usuário quer continuar
    response = input("\n\u2753 Deseja continuar com o upload e população? (s/n): ")
    if response.lower() not in ['s', 'sim', 'y', 'yes']:
        print("\u274c Operação cancelada.")
        sys.exit(0)
    
    # Upload de assets
    uploaded_files = upload_assets()
    
    # Popula o banco de dados
    populate_database(uploaded_files)
    
    print("\n\u2705 Processo concluído com sucesso!")
    print("="*60)
    print("\nPróximos passos:")
    print("  1. Verifique os arquivos no Azure Storage")
    print("  2. Verifique os dados no CosmosDB")
    print("  3. Teste a API do Azure Functions")
    print(f"     {FUNCTION_APP_URL}")

if __name__ == '__main__':
    main()
