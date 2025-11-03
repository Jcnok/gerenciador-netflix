import logging
import azure.functions as func
import json
from azure.storage.blob import BlobServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Função upload_file processando requisição.')

    try:
        # Obter arquivo do request
        file_data = req.get_body()
        filename = req.params.get('filename')
        
        if not filename:
            return func.HttpResponse(
                json.dumps({"error": "Parâmetro 'filename' não fornecido"}),
                status_code=400,
                mimetype="application/json"
            )

        # Conectar ao Blob Storage
        connection_string = os.environ['AzureWebJobsStorage']
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name = "netflix-catalogs"
        
        # Upload do arquivo
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        blob_client.upload_blob(file_data, overwrite=True)

        return func.HttpResponse(
            json.dumps({"message": f"Arquivo {filename} enviado com sucesso"}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f'Erro ao processar upload: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
