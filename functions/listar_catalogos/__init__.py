import logging
import azure.functions as func
import json
from azure.cosmos import CosmosClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Função listar_catalogos processando requisição.')

    try:
        # Conectar ao Cosmos DB
        cosmos_endpoint = os.environ['COSMOS_ENDPOINT']
        cosmos_key = os.environ['COSMOS_KEY']
        database_name = os.environ.get('COSMOS_DATABASE', 'NetflixDB')
        container_name = os.environ.get('COSMOS_CONTAINER', 'catalogs')
        
        client = CosmosClient(cosmos_endpoint, cosmos_key)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        
        # Listar todos os catálogos
        items = list(container.read_all_items())

        return func.HttpResponse(
            json.dumps({"catalogs": items}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f'Erro ao listar catálogos: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
