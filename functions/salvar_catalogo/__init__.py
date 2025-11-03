import logging
import azure.functions as func
import json
from azure.cosmos import CosmosClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Função salvar_catalogo processando requisição.')

    try:
        # Obter dados do request
        req_body = req.get_json()
        
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "Dados não fornecidos"}),
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
        
        # Salvar no Cosmos DB
        result = container.create_item(body=req_body)

        return func.HttpResponse(
            json.dumps({"message": "Catálogo salvo com sucesso", "id": result['id']}),
            status_code=201,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f'Erro ao salvar catálogo: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
