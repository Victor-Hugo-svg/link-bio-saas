from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Pages Service - Link na Bio",
    description="Microsserviço responsável por gerenciar páginas de criadores, SEO e captura de leads."
)

# Ativa a coleta automática de métricas para o Prometheus (Observabilidade)
Instrumentator().instrument(app).expose(app)

# Banco em memória simples para testes iniciais
pages_db = {
    "criador1": {
        "nome": "Criador Exemplo",
        "seo_title": "Links Oficiais - Criador Exemplo",
        "links": [{"id": 1, "titulo": "Meu Canal", "url": "https://youtube.com"}]
    }
}
leads_db = []

class Lead(BaseModel):
    criador: str
    email: str

@app.get("/pages/{username}", summary="Busca a página pública do criador")
def get_page(username: str):
    """Retorna os mini blocos de conteúdo e metadados de SEO da página."""
    return pages_db.get(username, {"erro": "Página não encontrada"})

@app.post("/leads", summary="Captura um novo lead (newsletter)")
def capture_lead(lead: Lead):
    """Salva o e-mail de um visitante interessado no conteúdo do criador."""
    leads_db.append(lead.dict())
    return {"mensagem": "Lead capturado com sucesso!", "total_leads": len(leads_db)}