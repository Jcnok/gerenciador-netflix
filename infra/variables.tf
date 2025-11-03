variable "resource_group_name" {
  description = "Nome do Resource Group"
  type        = string
  default     = "rg-netflix-catalog"
}

variable "location" {
  description = "Localização dos recursos Azure"
  type        = string
  default     = "brazilsouth"
}

variable "storage_account_name" {
  description = "Nome da Storage Account"
  type        = string
  default     = "stnetflixcatalog"
}

variable "cosmosdb_account_name" {
  description = "Nome da conta CosmosDB"
  type        = string
  default     = "cosmos-netflix-catalog"
}

variable "cosmosdb_database_name" {
  description = "Nome do banco de dados CosmosDB"
  type        = string
  default     = "NetflixDB"
}

variable "app_service_plan_name" {
  description = "Nome do App Service Plan"
  type        = string
  default     = "asp-netflix-catalog"
}

variable "function_app_name" {
  description = "Nome do Function App"
  type        = string
  default     = "func-netflix-catalog"
}
