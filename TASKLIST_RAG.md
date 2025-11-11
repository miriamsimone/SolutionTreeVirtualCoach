## Task List 3: RAG Database (Pinecone + Document Ingestion)

**Owner:** RAG/Data Engineer  
**Parallel Start:** Immediately

### Project Structure
```
rag/
├── data/
│   ├── raw/
│   │   ├── behavior_academies.txt          [INGEST]
│   │   ├── learning_by_doing.txt           [INGEST]
│   │   ├── the_way_forward.txt             [INGEST]
│   │   ├── essential_standards_2nd_math.txt [INGEST]
│   │   ├── american_gov_smartgoals.txt     [INGEST]
│   │   ├── 3rd_grade_smartgoals.txt        [INGEST]
│   ├── processed/
│   │   ├── embeddings_manifest.json        [CREATE]
├── scripts/
│   ├── ingest.py                           [CREATE]
│   ├── chunk_documents.py                  [CREATE]
│   ├── upload_to_pinecone.py               [CREATE]
│   ├── validate_embeddings.py              [CREATE]
│   ├── metadata_tagger.py                  [CREATE]
├── config/
│   ├── __init__.py                         [CREATE]
│   ├── pinecone_config.py                  [CREATE]
│   ├── document_config.py                  [CREATE]
├── utils/
│   ├── __init__.py                         [CREATE]
│   ├── text_processor.py                   [CREATE]
│   ├── embedding_handler.py                [CREATE]
├── requirements.txt                        [CREATE]
├── .env.example                            [CREATE]
└── README.md                               [CREATE]

```

### Key Deliverables

1. **Document Chunking** (`scripts/chunk_documents.py`)
   - Parse raw text documents into semantic chunks (300-500 tokens)
   - Preserve document boundaries and section headers
   - Store chunk metadata (doc_name, page/section, chunk_index)

2. **Metadata Tagging** (`scripts/metadata_tagger.py`)
   - Tag each chunk with agent affinity:
     - `agent: "professional_learning"` (for Behavior Academies, Learning by Doing, The Way Forward)
     - `agent: "curriculum_planning"` (for Standards, SmartGoals docs)
   - Include document source metadata (title, chapter, section)
   - Allow for document overlap (chunk can belong to multiple agents)

3. **Embedding Generation** (`utils/embedding_handler.py`)
   - Use OpenAI embedding API to generate vectors for each chunk
   - Batch processing for efficiency
   - Error handling and retry logic

4. **Pinecone Index Setup** (`scripts/upload_to_pinecone.py`)
   - Create Pinecone index with appropriate dimension (1536 for OpenAI)
   - Configure metadata indexing (for filtering by agent, doc_name, etc.)
   - Upload embeddings with metadata to Pinecone
   - Verify successful upload

5. **Metadata Filtering Configuration** (`config/document_config.py`)
   - Define which documents belong to which agents
   - Store document-to-agent mappings
   - Define filtering criteria for Pinecone queries

6. **Document Validation** (`scripts/validate_embeddings.py`)
   - Test that embeddings are correctly stored in Pinecone
   - Verify metadata filtering works (retrieve by agent type)
   - Run sample queries to ensure retrieval quality
   - Generate validation report

7. **Text Processing Utilities** (`utils/text_processor.py`)
   - Clean and normalize text
   - Handle special characters and formatting
   - Preserve important structure (headings, lists, etc.)

8. **Configuration Management** (`config/pinecone_config.py`)
   - Pinecone API credentials and index name
   - Embedding model configuration
   - Chunk size and overlap settings
   - Metadata schema definition

### Files to Edit During Development
- `requirements.txt` — Add dependencies (pinecone-client, openai, python-dotenv, etc.)
- `.env.example` — Document Pinecone API key, index name, OpenAI API key

### Integration Points
- Raw documents provided by Solution Tree (placed in `data/raw/`)
- OpenAI API for embeddings
- Pinecone index accessed by backend service
- Backend queries Pinecone using metadata filters for agent routing

### Agent-Specific Metadata Schema (Example)
```
Metadata for each chunk:
{
  "doc_name": "behavior_academies",
  "agent": ["professional_learning"],  // or ["curriculum_planning"] or both
  "section": "Chapter 3: Team Dynamics",
  "chunk_index": 5,
  "page_ref": "45-47"
}
```

