# Define directories
DOCUMENTS_DIR := "documents"
VECTOR_STORE_DIR := "vector_store"
MODELS_DIR := "models"
LOGS_DIR = "logs"
ARTIFACTS_DIR := "artifacts"

.PHONY: install app clean help

SHELL = /bin/bash
.SHELLFLAGS = -ec

install:
	@echo "Installing Dependencies..."
#	@python -m venv .venv
#	@.venv\Scripts\activate
	@pip install -r requirements.txt

app:
	@echo "Run web interface..."
	@python -m app

clean:
	@echo "Deleting Files..."
ifeq ($(OS),Windows_NT)
	-@if exist $(DOCUMENTS_DIR) rmdir /s /q $(DOCUMENTS_DIR)
	-@if exist $(VECTOR_STORE_DIR) rmdir /s /q $(VECTOR_STORE_DIR)
	-@if exist $(LOGS_DIR) rmdir /s /q $(LOGS_DIR)
	-@if exist $(ARTIFACTS_DIR) rmdir /s /q $(ARTIFACTS_DIR)
else
	-@rm -rf $(DOCUMENTS_DIR) $(VECTOR_STORE_DIR) $(LOGS_DIR) $(ARTIFACTS_DIR) 2>/dev/null || true
endif


help:
	@echo "Available targets:"
	@echo "  install                : Install dependencies from requirements.txt"
	@echo "  app                	: Run web interface"
	@echo "  clean                  : Clean up the project directory by removing generated files and directories"
	@echo "  help                   : Display this help message"
