from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Analytics Service - Rastreamento de Links",
    description="Microsserviço responsável por contabilizar cliques e desempenho de campanhas."
)

Instrumentator().instrument(app).expose(app)

clicks_db = {}

@app.post("/track/{link_id}", summary="Registra um clique em um link")
def track_click(link_id: str):
    """Incrementa o contador de cliques para o link especificado."""
    clicks_db[link_id] = clicks_db.get(link_id, 0) + 1
    return {"link_id": link_id, "total_cliques": clicks_db[link_id]}

@app.get("/stats", summary="Retorna o painel de desempenho dos links")
def get_stats():
    """Exibe o total de cliques registrados por link."""
    return {"desempenho": clicks_db}