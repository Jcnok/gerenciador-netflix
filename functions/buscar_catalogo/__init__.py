import logging
import azure.functions as func
import json
from azure.cosmos import CosmosClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Função buscar_catalogo processando requisição.')

    try:
        # Obter ID do request
        catalog_id = req.params.get('id')
        
        if not catalog_id:
            return func.HttpResponse(
                json.dumps({"error": "Parâmetro 'id' não fornecido"}),
                status_code=400,
                mimetype="application/json"
            )

        # Conectar ao Cosmos DB
        cosmos_endpoint = os.environ['COSMOS_ENDPOINT']
        cosmos_key = os.environ['COSMOS_KEY']
        database_name = os.environ.get('COSMOS_DATABASE', 'NetflixDB')
        container_name = os.environ.get('COSMOS_CONTAINER', 'catalogs')
        
        client = CosmosClient(cosmos_endpoint, cosmos_key)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        
        # Buscar catálogo por ID
        item = container.read_item(item=catalog_id, partition_key=catalog_id)

        return func.HttpResponse(
            json.dumps({"catalog": item}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f'Erro ao buscar catálogo: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
