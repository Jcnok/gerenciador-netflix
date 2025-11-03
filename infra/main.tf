# Configuração do Provider Azure
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "netflix_rg" {
  name     = var.resource_group_name
  location = var.location
}

# Storage Account
resource "azurerm_storage_account" "netflix_storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.netflix_rg.name
  location                 = azurerm_resource_group.netflix_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Storage Container for Thumbnails
resource "azurerm_storage_container" "thumbnails" {
  name                  = "thumbnails"
  storage_account_name  = azurerm_storage_account.netflix_storage.name
  container_access_type = "blob"
}

# Storage Container for Videos
resource "azurerm_storage_container" "videos" {
  name                  = "videos"
  storage_account_name  = azurerm_storage_account.netflix_storage.name
  container_access_type = "blob"
}

# CosmosDB Account
resource "azurerm_cosmosdb_account" "netflix_cosmos" {
  name                = var.cosmosdb_account_name
  location            = azurerm_resource_group.netflix_rg.location
  resource_group_name = azurerm_resource_group.netflix_rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.netflix_rg.location
    failover_priority = 0
  }
}

# CosmosDB SQL Database
resource "azurerm_cosmosdb_sql_database" "netflix_db" {
  name                = var.cosmosdb_database_name
  resource_group_name = azurerm_resource_group.netflix_rg.name
  account_name        = azurerm_cosmosdb_account.netflix_cosmos.name
  throughput          = 400
}

# CosmosDB SQL Container for Movies
resource "azurerm_cosmosdb_sql_container" "movies" {
  name                = "movies"
  resource_group_name = azurerm_resource_group.netflix_rg.name
  account_name        = azurerm_cosmosdb_account.netflix_cosmos.name
  database_name       = azurerm_cosmosdb_sql_database.netflix_db.name
  partition_key_path  = "/id"
  throughput          = 400
}

# Azure Functions
resource "azurerm_service_plan" "netflix_plan" {
  name                = var.app_service_plan_name
  location            = azurerm_resource_group.netflix_rg.location
  resource_group_name = azurerm_resource_group.netflix_rg.name
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "netflix_functions" {
  name                       = var.function_app_name
  location                   = azurerm_resource_group.netflix_rg.location
  resource_group_name        = azurerm_resource_group.netflix_rg.name
  service_plan_id            = azurerm_service_plan.netflix_plan.id
  storage_account_name       = azurerm_storage_account.netflix_storage.name
  storage_account_access_key = azurerm_storage_account.netflix_storage.primary_access_key

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "COSMOSDB_ENDPOINT"   = azurerm_cosmosdb_account.netflix_cosmos.endpoint
    "COSMOSDB_KEY"        = azurerm_cosmosdb_account.netflix_cosmos.primary_key
    "COSMOSDB_DATABASE"   = azurerm_cosmosdb_sql_database.netflix_db.name
    "COSMOSDB_CONTAINER"  = azurerm_cosmosdb_sql_container.movies.name
    "STORAGE_ACCOUNT_URL" = azurerm_storage_account.netflix_storage.primary_blob_endpoint
  }
}
