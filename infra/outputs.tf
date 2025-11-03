output "resource_group_name" {
  description = "Nome do Resource Group criado"
  value       = azurerm_resource_group.netflix_rg.name
}

output "storage_account_name" {
  description = "Nome da Storage Account criada"
  value       = azurerm_storage_account.netflix_storage.name
}

output "storage_account_primary_blob_endpoint" {
  description = "Endpoint primário do Blob Storage"
  value       = azurerm_storage_account.netflix_storage.primary_blob_endpoint
}

output "thumbnails_container_name" {
  description = "Nome do container de thumbnails"
  value       = azurerm_storage_container.thumbnails.name
}

output "videos_container_name" {
  description = "Nome do container de vídeos"
  value       = azurerm_storage_container.videos.name
}

output "cosmosdb_account_name" {
  description = "Nome da conta CosmosDB criada"
  value       = azurerm_cosmosdb_account.netflix_cosmos.name
}

output "cosmosdb_endpoint" {
  description = "Endpoint do CosmosDB"
  value       = azurerm_cosmosdb_account.netflix_cosmos.endpoint
  sensitive   = true
}

output "cosmosdb_database_name" {
  description = "Nome do banco de dados CosmosDB"
  value       = azurerm_cosmosdb_sql_database.netflix_db.name
}

output "cosmosdb_container_name" {
  description = "Nome do container de filmes no CosmosDB"
  value       = azurerm_cosmosdb_sql_container.movies.name
}

output "function_app_name" {
  description = "Nome do Function App criado"
  value       = azurerm_linux_function_app.netflix_functions.name
}

output "function_app_default_hostname" {
  description = "URL padrão do Function App"
  value       = azurerm_linux_function_app.netflix_functions.default_hostname
}
