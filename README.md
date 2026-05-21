# Manufacturing AI Co-pilot

An AI-powered operations assistant for manufacturing teams, built during a GenAI hackathon. It combines Azure OpenAI, Azure AI Search, and Streamlit to let operations teams ask plain-English questions about their production data and get intelligent, data-backed answers instantly.

---

## What It Does

Manufacturing teams deal with massive amounts of data every day — sensor readings, machine faults, downtime events, quality inspection results, and maintenance records. The problem is that this data sits in spreadsheets and systems that take too long to query, and by the time a report is generated, the problem has already cost time and money.

This co-pilot changes that. You connect it to your production data, and your team can simply ask:

- *"Which machine has the most downtime this week?"*
- *"What caused MACH-003 to go into fault?"*
- *"Which production line has the lowest efficiency?"*
- *"What maintenance actions reduced vibration spikes?"*

And get an answer in seconds not hours.

---

## How It Works

The system follows a four-step pipeline:

**Step 1 — Data Ingestion**
CSV files containing machine sensor logs, downtime events, quality inspections, maintenance records, and production summaries are uploaded to Azure Blob Storage.

**Step 2 — Vectorization and Indexing**
Each row of data is converted into a vector embedding using Azure OpenAI's `text-embedding-ada-002` model and indexed in Azure AI Search. This makes the data semantically searchable — meaning the system understands the meaning of a question, not just keywords.

**Step 3 — RAG Pipeline**
When a user asks a question, the system embeds the question, searches the index for the most relevant data records, and passes them to GPT-4o along with the question. The AI reasons over the real data and returns a grounded, specific answer.

**Step 4 — Streamlit Interface**
A two-tab web interface built with Streamlit. The first tab is an operations dashboard with charts and KPIs. The second tab is the conversational AI co-pilot where users type or click questions and get answers.

---

## Dataset

The project uses five generated manufacturing datasets that simulate a realistic production environment across five machines (`MACH-001` to `MACH-005`) and three production lines (`Line-A`, `Line-B`, `Line-C`) over 45 days:

| File | Rows | What It Contains |
|---|---|---|
| `sensor_logs.csv` | 2,000 | Temperature, vibration, pressure, machine status, fault types |
| `downtime_events.csv` | 120 | Downtime duration, root causes, resolution details |
| `quality_inspections.csv` | 800 | Units inspected, units passed, defect types |
| `maintenance_records.csv` | 200 | Task type, component, technician, cost, notes |
| `production_summary.csv` | 405 | Planned vs actual units, efficiency, scrap, shift |

The data includes injected fault conditions — overheating, vibration spikes, motor faults, and quality defects — so the AI has real patterns to reason about.

---

## Project Structure

```
GenAI_Manufacturing_Copilot/
│
├── .env                        # Azure credentials — never committed
├── .gitignore
├── requirements.txt
├── README.md
├── app.py                      # Streamlit UI — dashboard + AI chat
│
├── data/
│   ├── sensor_logs.csv
│   ├── downtime_events.csv
│   ├── quality_inspections.csv
│   ├── maintenance_records.csv
│   └── production_summary.csv
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Loads all environment variables
│   ├── blob_upload.py          # Uploads CSVs to Azure Blob Storage
│   ├── indexer.py              # Creates embeddings and indexes data
│   ├── rag_pipeline.py         # RAG query function
│   └── cosmos_db.py            # Saves chat history to Cosmos DB
│
└── scripts/
    ├── 01_upload_data.py       # Run first — uploads data to Azure
    ├── 02_create_index.py      # Run second — builds the search index
    └── 03_test_rag.py          # Run third — tests RAG before launching UI
```

---

## Azure Services Used

- **Azure Blob Storage** — stores the raw CSV files
- **Azure AI Search** — hosts the vector index for semantic search
- **Azure OpenAI** — provides GPT-4o for reasoning and `text-embedding-ada-002` for embeddings
- **Azure Cosmos DB** — stores chat history with session tracking
- **Microsoft Foundry** — used for model deployment and management

---

## Getting Started

### Prerequisites

- Python 3.11 or 3.12
- An Azure subscription with the services above provisioned
- VS Code (recommended)

### 1. Clone the repo

```bash
git clone https://github.com/NimahMasuud/manufacturing-ai-copilot.git
cd manufacturing-ai-copilot
```

### 2. Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

Create a `.env` file in the root folder and fill in your Azure credentials:

```
AZURE_STORAGE_CONN_STRING=
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_KEY=
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
COSMOS_ENDPOINT=
COSMOS_KEY=
COSMOS_DATABASE=manufacturing
COSMOS_CONTAINER=chat_history
```

### 5. Run the setup scripts in order

```bash
# Upload CSVs to Azure Blob Storage
python scripts/01_upload_data.py

# Create embeddings and build the search index
python scripts/02_create_index.py

# Test the RAG pipeline before launching the UI
python scripts/03_test_rag.py
```

### 6. Launch the app

```bash
streamlit run app.py
```

---

## Requirements

```
azure-storage-blob
azure-search-documents
azure-cosmos
openai
streamlit
pandas
plotly
python-dotenv
```

---

## What the Dashboard Shows

The operations dashboard tab includes:

- Total downtime events and total downtime minutes
- Average production efficiency across all lines
- Total defect units across all inspections
- Downtime by machine (bar chart)
- Downtime causes breakdown (pie chart)
- Temperature trends by machine over time (line chart)
- Quality pass rate by machine vs 80% target (bar chart)
- Production efficiency by line vs 80% target (bar chart)
- Maintenance cost by machine (bar chart)
- Scrap units over time by production line (area chart)

---

## What the AI Co-pilot Can Answer

The chat tab connects to the RAG pipeline and can answer questions like:

- Which machine has the highest downtime?
- What are the most common fault types?
- Which shift has the most machine warnings?
- What is the average maintenance cost per machine?
- Which production line is performing below the efficiency target?
- What defect types appear most in quality inspections?

Every answer is grounded in the actual indexed data — the AI does not guess.

---

## Built With

- Python 3.12
- Streamlit
- Azure OpenAI (GPT-4o + text-embedding-ada-002)
- Azure AI Search (vector search with HNSW)
- Azure Blob Storage
- Azure Cosmos DB
- Plotly for charts
- Pandas for data handling

---

## Author

Built by Nimah Masuud as part of a GenAI hackathon project focused on manufacturing operations intelligence.
