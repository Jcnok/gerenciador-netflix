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

# Azure Functions
resource "azurerm_service_plan" "netflix_plan" {
  name                = var.app_service_plan_name
  location            = azurerm_resource_group.netflix_rg.location
  resource_group_name = azurerm_resource_group.netflix_rg.name
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "netflix_functions" {
  name                = var.function_app_name
  location            = azurerm_resource_group.netflix_rg.location
  resource_group_name = azurerm_resource_group.netflix_rg.name
  service_plan_id     = azurerm_service_plan.netflix_plan.id
  storage_account_name       = azurerm_storage_account.netflix_storage.name
  storage_account_access_key = azurerm_storage_account.netflix_storage.primary_access_key

  site_config {
    application_stack {
      python_version = "3.9"
    }
  }
}
