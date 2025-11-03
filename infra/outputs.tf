output "resource_group_name" {
  description = "Nome do Resource Group criado"
  value       = azurerm_resource_group.netflix_rg.name
}

output "storage_account_name" {
  description = "Nome da Storage Account criada"
  value       = azurerm_storage_account.netflix_storage.name
}

output "function_app_name" {
  description = "Nome do Function App criado"
  value       = azurerm_linux_function_app.netflix_functions.name
}

output "function_app_default_hostname" {
  description = "URL padrão do Function App"
  value       = azurerm_linux_function_app.netflix_functions.default_hostname
}
