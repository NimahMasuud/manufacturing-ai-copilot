import os
import pandas as pd
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField,
    SearchField, SearchFieldDataType, VectorSearch,
    HnswAlgorithmConfiguration, VectorSearchProfile
)
from azure.core.credentials import AzureKeyCredential
from src.config import (
    SEARCH_ENDPOINT, SEARCH_KEY, OPENAI_KEY,
    OPENAI_ENDPOINT, EMBEDDING_DEPLOYMENT, INDEX_NAME
)

oai = AzureOpenAI(
    api_key=OPENAI_KEY,
    azure_endpoint=OPENAI_ENDPOINT,
    api_version="2024-02-01"
)

idx_client = SearchIndexClient(
    SEARCH_ENDPOINT,
    AzureKeyCredential(SEARCH_KEY)
)

def create_index():
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="source", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="myHnsw"
        )
    ]
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="myHnsw")],
        profiles=[VectorSearchProfile(
            name="myHnsw",
            algorithm_configuration_name="myHnsw"
        )]
    )
    idx_client.create_or_update_index(
        SearchIndex(name=INDEX_NAME, fields=fields, vector_search=vector_search)
    )
    print(f"Index '{INDEX_NAME}' created or updated.")

def embed_text(text):
    return oai.embeddings.create(
        input=text,
        model=EMBEDDING_DEPLOYMENT
    ).data[0].embedding

def index_csv(csv_file):
    search_client = SearchClient(
        SEARCH_ENDPOINT,
        INDEX_NAME,
        AzureKeyCredential(SEARCH_KEY)
    )
    df = pd.read_csv(csv_file)
    docs = []
    for i, row in df.iterrows():
        text = " | ".join([f"{k}: {v}" for k, v in row.items()])
        docs.append({
            "id": f"{os.path.basename(csv_file).replace('.', '-')}_{i}",
            "content": text,
            "source": csv_file,
            "embedding": embed_text(text)
        })
        if len(docs) >= 50:
            search_client.upload_documents(docs)
            docs = []
    if docs:
        search_client.upload_documents(docs)
    print(f"Indexed {len(df)} rows from {csv_file}")

def index_all(data_folder="data"):
    create_index()
    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):
            index_csv(os.path.join(data_folder, filename))