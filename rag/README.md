# RAG Database for PLC Coach

This directory contains the RAG (Retrieval-Augmented Generation) pipeline for the AI Powered PLC at Work Virtual Coach project. It handles document ingestion, chunking, embedding generation, and upload to Pinecone vector database.

## Project Structure

```
rag/
├── data/
│   ├── raw/                      # Source documents (7 files)
│   └── processed/                # Generated manifests and metadata
├── config/
│   ├── document_config.py        # Document-to-agent mappings
│   └── pinecone_config.py        # Pinecone connection handler
├── utils/
│   ├── text_processor.py         # Text cleaning utilities
│   └── embedding_handler.py      # OpenAI embedding generation
├── scripts/
│   ├── ingest.py                 # Main ingestion orchestrator
│   ├── chunk_documents.py        # Document chunking
│   ├── metadata_tagger.py        # Agent metadata tagging
│   ├── upload_to_pinecone.py     # Upload vectors to Pinecone
│   └── validate_embeddings.py    # Validation tests
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (API keys)
└── README.md                     # This file
```

## Setup

### 1. Install Dependencies

From the project root:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r rag/requirements.txt
```

### 2. Configure Environment Variables

The `.env` file should contain:
```
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=plc-coach
```

### 3. Source Documents

Place raw text documents in `rag/data/raw/`:
- `behavior_academies.txt`
- `learning_by_doing.txt`
- `learning_by_doing_actionguide.txt`
- `the_way_forward.txt`
- `essential_standards_2nd_math.txt`
- `american_gov_smartgoals.txt`
- `3rd_grade_smartgoals.txt`

## Usage

### Run Full Ingestion Pipeline

From the project root:
```bash
venv/bin/python rag/scripts/ingest.py
```

This will:
1. Chunk all documents into 400-token chunks with 50-token overlap
2. Tag each chunk with agent affinity metadata
3. Generate 1024-dimensional embeddings using OpenAI `text-embedding-3-small`
4. Upload vectors to Pinecone index `plc-coach`
5. Save embeddings manifest to `data/processed/embeddings_manifest.json`

**Expected Output:**
```
============================================================
RAG INGESTION PIPELINE
============================================================
STEP 1: Chunking documents
✓ Created 147 chunks from 7 documents

STEP 2: Tagging chunks with metadata
✓ Tagged 147 chunks

STEP 3: Generating embeddings
✓ Generated 147 embeddings

STEP 4: Uploading to Pinecone
✓ Uploaded 147 vectors to index 'plc-coach'

STEP 5: Saving embeddings manifest
✓ Saved embeddings manifest
============================================================
```

### Validate Embeddings

Run validation tests to ensure everything works:
```bash
venv/bin/python rag/scripts/validate_embeddings.py
```

This will test:
- Basic retrieval from Pinecone
- Agent-specific metadata filtering
- Document-specific filtering
- Index statistics

### Skip Upload (Testing)

To test chunking and embeddings without uploading to Pinecone:
```bash
venv/bin/python rag/scripts/ingest.py --skip-upload
```

## Agent-Document Mappings

### Professional Learning Agent
- `behavior_academies.txt`
- `learning_by_doing.txt`
- `learning_by_doing_actionguide.txt`
- `the_way_forward.txt`

### Curriculum Planning Agent
- `essential_standards_2nd_math.txt`
- `american_gov_smartgoals.txt`
- `3rd_grade_smartgoals.txt`

## Technical Details

### Chunking Strategy
- **Chunk size:** 400 tokens
- **Overlap:** 50 tokens
- **Method:** Sentence-boundary aware chunking
- Text is cleaned and normalized while preserving structure (lists, headings)

### Embeddings
- **Model:** `text-embedding-3-small`
- **Dimensions:** 1024 (configured for Pinecone index)
- **Batch size:** 100 texts per API call
- Includes retry logic with exponential backoff

### Metadata Schema
Each vector in Pinecone includes:
```python
{
  "doc_name": "learning_by_doing.txt",
  "doc_title": "Learning by Doing",
  "chunk_index": 5,
  "token_count": 387,
  "text": "chunk text preview...",
  "agent_professional_learning": True,  # or agent_curriculum_planning
}
```

### Filtering in Backend
To retrieve chunks for a specific agent:
```python
results = index.query(
    vector=query_embedding,
    top_k=5,
    filter={"agent_professional_learning": True}
)
```

## Troubleshooting

### API Key Issues
- Ensure `.env` file is in `rag/` directory
- Check that API keys are valid and have appropriate permissions

### Dimension Mismatch
- Pinecone index must be created with dimension=1024
- If you need to change dimensions, delete and recreate the index

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Statistics

After successful ingestion:
- **Total documents:** 7
- **Total chunks:** 147
- **Average chunk size:** ~350 tokens
- **Pinecone index:** `plc-coach` (1024 dimensions, cosine metric)

## Next Steps

The backend FastAPI service will:
1. Accept user queries
2. Determine which agent to use (Professional Learning or Curriculum Planning)
3. Generate query embeddings
4. Query Pinecone with appropriate metadata filters
5. Return relevant chunks with citations for the LLM to use in responses
