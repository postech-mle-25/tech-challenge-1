class DB:
    INDEX_COLUMNS_MAP = {
        "Comercio": ["control", "produto", "ano"],
        "Exporta": ["pais", "tipo", "ano"],
        "Importa": ["pais", "tipo", "ano"],
        "Processamento": ["control", "cultivar", "tipo", "ano"],
        "Producao": ["control", "produto", "ano"],
    }
