# KnowNetQA: Information Retrieval and Analysis System

## Table of Contents

  * [1. Project Overview](#1-project-overview)
  * [2. System Architecture](#2-system-architecture)
  * [3. Key Features](#3-key-features)
  * [4. Gradio Web Application](#4-gradio-web-application)
  * [5. Getting Started](#5-getting-started)
  * [6. Project Structure](#6-project-structure)
  * [7. Usage](#7-usage)
  * [8. Acknowledgments](#8-acknowledgments)

## 1. Project Overview

KnowNetQA is an advanced information retrieval and analysis system designed to intelligently extract, analyze, and respond to user queries from various documents on the web. By integrating state-of-the-art NLP techniques and machine learning models, KnowNetQA aims to streamline the process of gaining insights from vast amounts of unstructured text data.

## 2. System Architecture

Below is a high-level diagram that illustrates the architecture of the KnowNetQA system:

![KnowNetQA System Diagram](/images/system_architecture.png)

This architecture is designed to streamline the process of extracting and analyzing information in response to user queries. It depicts the workflow from initial query to the delivery of a refined answer, facilitated by the interplay between web scraping, data processing, and response generation.

## 3. Key Features

KnowNetQA integrates a suite of advanced technologies and libraries to deliver precise information retrieval and analysis:

- **Keyword Extraction and Analysis:** Utilizes [spaCy](https://spacy.io/models), a powerful NLP library, to extract key terms and phrases from user queries to guide the subsequent retrieval process.

- **Web Scraping & Document Retrieval:** Engages [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) Automated web scraping is performed to gather documents from specified web sources, laying the groundwork for information extraction and processing.

- **Document Processing:** Employs [spaCy](https://spacy.io/models) for initial text processing and the [TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) algorithm for document vectorization, ensuring that the content fetched via web scraping is effectively processed for relevance and redundancy checks.

- **Embedding and Vectorization:** Leverages [Hugging Face](https://huggingface.co/sentence-transformers)'s embedding models to convert text documents into numerical vectors, enabling efficient retrieval and comparison within the vector database.

- **Intelligent Prompt Creation:** Implements dynamic prompt templates that inform the creation of prompts based on the user's query and context from retrieved documents.

- **Large Language Model Integration:** Incorporates C/C++ inference implementation of [LLaMa 2](https://github.com/ggerganov/llama.cpp), a state-of-the-art large language model, for generating informed responses based on the user's query and relevant document context.

- **Contextual Response Generation:** Ensures responses are not only accurate but contextually relevant, utilizing the [LangChain](https://python.langchain.com/docs/get_started/introduction) framework to integrate the LLM with the knowledge retrieved.

- **Gradio Interface for Interactivity:** Provides an interactive [Gradio](https://www.gradio.app/guides/quickstart) web interface for users to input queries and receive real-time responses, making the system more accessible and user-friendly.

## 4. Gradio Web Application

KnowNetQA includes an interactive Gradio web application for a user-friendly interface to submit queries and receive responses:

![Gradio Web Application Screenshot](/images/gradio_app_screenshot.png)


## 5. Getting Started

To set up KnowNetQA on your local machine, follow these steps:

1. **Clone the repository**

   ```bash
   git clone https://github.com/riaa3102/KnowNetQA.git
   ```

2. **Install the required dependencies**

Navigate to the project directory and run:

   ```bash
   make install
   ```

## 6. Project Structure

    KnowNetQA/
    ├── documents/              # Directory for extracted documents
    │   └── extracted.txt       # Example of an extracted document
    ├── logs/                   # Directory for logger
    │   └── logs.txt
    ├── app.py                  # Main entry point of the application
    ├── Makefile                # Makefile for automating commands
    ├── models/                 # Trained models and embeddings
    │   └── llama-2-7b-chat.Q2_K.gguf
    ├── README.md               # Project documentation
    ├── requirements.txt        # Project dependencies
    └── src/                    # Source code
        ├── __init__.py
        ├── chatbot.py
        ├── config.yaml         # Configuration settings
        ├── dirs.py             # Directory path configurations
        ├── document_extractor.py
        ├── document_loader.py
        ├── embeddings_manager.py
        ├── keyword_extractor.py
        ├── utils.py            # Utility functions
        ├── vector_store_manager.py
        └── web_interface.py    # Web interface for interaction


## 7. Usage

### Running KnowNetQA

To run the KnowNetQA system and start the web interface:

   ```bash
   make app
   ```
After starting the system, you can interact with the KnowNetQA web interface by opening your web browser and navigating to:

- **Light Theme:** [localhost:8080](http://127.0.0.1:8080)
- **Dark Theme:** [localhost:8080/?__theme=dark](http://127.0.0.1:8080/?__theme=dark)

The web interface provides a user-friendly way to submit queries and view the system's responses.

### Cleaning Up

To clean up and remove any generated files and directories created during the usage of KnowNetQA, you can use the following command:

   ```bash
   make clean
   ```

This command helps maintain a clean working environment by removing temporary files and outputs.

### Debugging and Logging

KnowNetQA provides detailed logs during execution, which can be helpful for debugging purposes or to gain insights into the system's operational flow. Logs are stored in the logs directory and can be reviewed for troubleshooting or analysis.

For more detailed usage instructions, command options, and system configuration, refer to the individual script documentation within the src directory.

##  8. Acknowledgments

Special thanks are extended to the developers and maintainers of the open-source tools and datasets utilized in this project.