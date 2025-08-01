from functools import lru_cache

from elasticsearch import AsyncElasticsearch

from src.core.config import settings


@lru_cache
def get_elastic_client() -> AsyncElasticsearch:
    return AsyncElasticsearch(settings.ELASTICSEARCH_HOSTS)
