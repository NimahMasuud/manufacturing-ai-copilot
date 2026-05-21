import os
from dotenv import load_dotenv

load_dotenv()

STORAGE_CONN_STRING     = os.getenv("AZURE_STORAGE_CONN_STRING")
SEARCH_ENDPOINT         = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY              = os.getenv("AZURE_SEARCH_KEY")
OPENAI_ENDPOINT         = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_KEY              = os.getenv("AZURE_OPENAI_KEY")
OPENAI_DEPLOYMENT       = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
EMBEDDING_DEPLOYMENT    = os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
CONTAINER_NAME          = "manufacturing-data"
INDEX_NAME              = "manufacturing-index"