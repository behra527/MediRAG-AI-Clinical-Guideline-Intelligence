import hashlib
import re
from functools import lru_cache
from pathlib import Path
import chromadb
import fitz
from sentence_transformers import SentenceTransformer
from .core import STORAGE

@lru_cache
def embedder():
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

@lru_cache
def collection():
    client = chromadb.PersistentClient(path=str(STORAGE / 'chroma'))
    return client.get_or_create_collection('guidelines', metadata={'hnsw:space': 'cosine'})

def split_text(text, chunk_size=950, overlap=150):
    if chunk_size <= overlap or overlap < 0: raise ValueError('Invalid chunk settings')
    text = re.sub(r'\s+', ' ', text).strip()
    if not text: return []
    chunks=[]; start=0
    while start < len(text):
        end=min(start+chunk_size,len(text))
        if end < len(text):
            boundary=text.rfind(' ', start+int(chunk_size*.6), end)
            if boundary>start: end=boundary
        chunks.append(text[start:end].strip())
        if end==len(text): break
        start=max(start+1,end-overlap)
    return [c for c in chunks if c]

def ingest_pdf(data: bytes, filename: str):
    try:
        pdf=fitz.open(stream=data,filetype='pdf')
    except Exception as exc: raise ValueError('Cannot read this PDF') from exc
    doc_id=hashlib.sha256(data).hexdigest()[:20]
    items=[]
    page_no=0
    for page_no,page in enumerate(pdf,1):
        for index,chunk in enumerate(split_text(page.get_text('text'))):
            items.append((f'{doc_id}:{page_no}:{index}',chunk,{'document_id':doc_id,'filename':filename,'page':page_no,'chunk':index}))
    pdf.close()
    if not items: raise ValueError('No extractable text. Scanned PDFs need OCR.')
    col=collection()
    # Replace old chunks of the same document, preserving stable IDs.
    old=col.get(where={'document_id':doc_id})['ids']
    if old: col.delete(ids=old)
    for i in range(0,len(items),64):
        batch=items[i:i+64]
        vectors=embedder().encode([x[1] for x in batch],normalize_embeddings=True).tolist()
        col.upsert(ids=[x[0] for x in batch],documents=[x[1] for x in batch],metadatas=[x[2] for x in batch],embeddings=vectors)
    return {'document_id':doc_id,'filename':filename,'pages':page_no,'chunks':len(items)}

def retrieve(query: str, top_k: int=5, document_id: str|None=None):
    col=collection()
    if not col.count(): return []
    vector=embedder().encode([query],normalize_embeddings=True).tolist()[0]
    opts={'query_embeddings':[vector],'n_results':min(top_k,col.count()),'include':['documents','metadatas','distances']}
    if document_id: opts['where']={'document_id':document_id}
    try: result=col.query(**opts)
    except Exception as exc: raise RuntimeError(f'Retrieval failed: {exc}') from exc
    return [{'id':id,'text':text,'filename':meta['filename'],'page':meta['page'],'score':round(1-float(distance),3)} for id,text,meta,distance in zip(result['ids'][0],result['documents'][0],result['metadatas'][0],result['distances'][0])]

def documents():
    col=collection(); result=col.get(include=['metadatas']); found={}
    for meta in result['metadatas']:
        id=meta['document_id']; found.setdefault(id,{'document_id':id,'filename':meta['filename'],'chunks':0}); found[id]['chunks']+=1
    return list(found.values())

def delete_document(doc_id):
    col=collection(); ids=col.get(where={'document_id':doc_id})['ids']
    if ids: col.delete(ids=ids)
    return bool(ids)
