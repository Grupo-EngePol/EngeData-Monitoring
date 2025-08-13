# utils/cache_df.py
from flask_caching import Cache
from functools import lru_cache
from uuid import uuid4
import pandas as pd

# Cache global (inicializa no app)
cache = Cache(config={
    "CACHE_TYPE": "SimpleCache",          # produção: use Redis/Memcached
    "CACHE_DEFAULT_TIMEOUT": 3600,        # 1h
})

def init_cache(server):
    """Chame uma vez na inicialização: init_cache(app.server)"""
    cache.init_app(server)

def put_df(df: pd.DataFrame) -> str:
    """Guarda DF e retorna uma chave única."""
    key = f"df:{uuid4().hex}"
    cache.set(key, df)
    return key

def get_df(key: str) -> pd.DataFrame:
    """Busca DF do cache (sem LRU)."""
    df = cache.get(key)
    return df if df is not None else pd.DataFrame()

@lru_cache(maxsize=128)
def get_df_cached(key: str) -> pd.DataFrame:
    """Memo de 2º nível (por processo) para acelerar leituras repetidas."""
    return get_df(key)

def delete_df(key: str) -> None:
    try:
        cache.delete(key)
    except Exception:
        pass
