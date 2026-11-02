from typing import Literal
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
from .core import settings
from .rag import ingest_pdf, retrieve, documents, delete_document
from .llm import generate

app=FastAPI(title='MediRAG API',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=[s.strip() for s in settings().cors_origins.split(',')],allow_credentials=False,allow_methods=['GET','POST','DELETE'],allow_headers=['*'])

class Query(BaseModel):
    question: str=Field(min_length=3,max_length=3000)
    document_id: str|None=None
    top_k: int=Field(default=5,ge=1,le=10)

@app.get('/api/health')
def health(): return {'status':'ok','model':settings().openrouter_model}

@app.get('/api/documents')
def list_documents(): return documents()

@app.delete('/api/documents/{document_id}')
def remove(document_id: str):
    if not delete_document(document_id): raise HTTPException(404,'Document not found')
    return {'deleted':True}

@app.post('/api/upload')
async def upload(file: UploadFile=File(...)):
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400,'Upload a PDF file')
    max_size=settings().max_upload_mb*1024*1024
    data=await file.read(max_size+1)
    if len(data)>max_size: raise HTTPException(413,'PDF exceeds size limit')
    if not data.startswith(b'%PDF-'): raise HTTPException(400,'Invalid PDF header')
    try: return ingest_pdf(data,file.filename[:120])
    except ValueError as e: raise HTTPException(422,str(e))
    except Exception as e: raise HTTPException(500,f'Document indexing failed: {type(e).__name__}: {str(e)[:240]}')

async def answer(q:Query,mode:Literal['rag','baseline']):
    sources=retrieve(q.question,q.top_k,q.document_id) if mode=='rag' else []
    if mode=='rag' and not sources:
        return {'answer':'Not found in the uploaded guideline. Upload a searchable PDF or choose another document.','sources':[],'mode':mode}
    try: response=await generate(q.question,sources,mode=='rag')
    except httpx.HTTPStatusError as e: raise HTTPException(502,f'OpenRouter returned HTTP {e.response.status_code}')
    except (httpx.RequestError,RuntimeError,KeyError,IndexError,ValueError) as e: raise HTTPException(502,str(e))
    return {'answer':response,'sources':sources,'mode':mode}

@app.post('/api/chat')
async def chat(q:Query): return await answer(q,'rag')

@app.post('/api/compare')
async def compare(q:Query):
    baseline=await answer(q,'baseline')
    rag=await answer(q,'rag')
    return {'without_rag':baseline,'with_rag':rag,'note':'Judge correctness against the official guideline; do not assume RAG is always correct.'}
