from elasticsearch import AsyncElasticsearch

from src.core.config import settings

from .mappings import ALERT_INDEX_MAPPING


async def create_alert_index() -> None:
    async with AsyncElasticsearch(settings.ELASTICSEARCH_HOSTS) as es:
        exists = await es.indices.exists(index='alerts')
        if not exists.body:
            await es.indices.create(index='alerts', body=ALERT_INDEX_MAPPING)
