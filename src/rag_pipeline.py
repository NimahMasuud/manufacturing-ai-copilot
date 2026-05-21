from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from src.config import (
    SEARCH_ENDPOINT, SEARCH_KEY, OPENAI_KEY,
    OPENAI_ENDPOINT, OPENAI_DEPLOYMENT,
    EMBEDDING_DEPLOYMENT, INDEX_NAME
)

oai = AzureOpenAI(
    api_key=OPENAI_KEY,
    azure_endpoint=OPENAI_ENDPOINT,
    api_version="2024-02-01"
)

search_client = SearchClient(
    SEARCH_ENDPOINT,
    INDEX_NAME,
    AzureKeyCredential(SEARCH_KEY)
)

SYSTEM_PROMPT = """You are a manufacturing operations AI assistant.
You have access to real sensor logs, downtime events, quality inspections,
maintenance records, and production summaries.
When answering, cite specific data points from the context provided.
Suggest root causes and actionable recommendations.
Be concise but insightful."""

def rag_query(user_question: str) -> str:
    # Step 1 - embed the question
    q_vector = oai.embeddings.create(
        input=user_question,
        model=EMBEDDING_DEPLOYMENT
    ).data[0].embedding

    # Step 2 - retrieve top relevant documents
    results = search_client.search(
        search_text=user_question,
        vector_queries=[VectorizedQuery(
            vector=q_vector,
            k_nearest_neighbors=5,
            fields="embedding"
        )],
        top=5
    )
    context = "\n\n".join([r["content"] for r in results])

    # Step 3 - send to GPT-4o with context
    response = oai.chat.completions.create(
        model=OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_question}"}
        ]
    )
    return response.choices[0].message.content