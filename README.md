# Confluence RAG Builder

This project is designed to build a RAG (Red Amber Green) system using data parsed from a Confluence space. 

## Setup

1. Ensure you have Python 3.8 or higher installed.
2. Clone this repository.
3. Navigate to the project directory and install the requirements:

```
pip install -r requirements.txt
```

4. Copy the `config.template.yaml` to `config.yaml` and update the `base_url` with your Confluence space URL.
5. Run the data parser to collect data from Confluence:

```
python -m confluence_rag_builder.data_parser
```


(Additional setup steps and usage details can be added as the project evolves.)

...
## Modules

### Confluence Data Parser

This module is responsible for parsing and collecting data from a Confluence space. 
For a detailed walkthrough, see the [Data Parser Vignette](vignettes/data_parser_vignette.md).
To run it:
```
python -m confluence_rag_builder.data_parser
```

### Chatbot
To run the chatbot:
```
streamlit run chatbot_app.py
```

## License

Apache 2

