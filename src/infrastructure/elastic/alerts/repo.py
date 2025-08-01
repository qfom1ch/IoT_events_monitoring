from typing import Any

from elasticsearch.helpers import async_bulk

from src.core.clients.elastic import get_elastic_client
from src.domain.alerts.entities.alert import Alert
from src.domain.alerts.interfaces.alert_search_repo import AlertSearchRepo
from src.domain.alerts.value_objects.alert_id import AlertId
from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.sensor_events.value_objects.sensor_event_id import SensorEventId

from .indices import create_alert_index
from .mappers import alert_to_document
from .schemas import AlertSearchQuery


class ElasticAlertSearchRepo(AlertSearchRepo):
    def __init__(self) -> None:
        self.es = get_elastic_client()

    async def search(self, query: AlertSearchQuery) -> list[Alert]:
        await create_alert_index()

        must_clauses = []
        filter_clauses = []

        if query.query:
            must_clauses.append({'match': {'message': query.query}})

        if query.device_id:
            filter_clauses.append({'term': {'device_id': query.device_id}})

        if query.severity is not None:
            filter_clauses.append({'term': {'severity': query.severity}})

        if query.min_severity is not None:
            filter_clauses.append({'range': {'severity': {'gte': query.min_severity}}})

        if query.created_from or query.created_to:
            range_filter = {}
            if query.created_from:
                range_filter['gte'] = query.created_from.isoformat()
            if query.created_to:
                range_filter['lte'] = query.created_to.isoformat()
            filter_clauses.append({'range': {'created_at': range_filter}})

        bool_query = {}
        if must_clauses:
            bool_query['must'] = must_clauses
        if filter_clauses:
            bool_query['filter'] = filter_clauses

        body = {
            'query': {'bool': bool_query},
            'from': query.page * query.size,
            'size': query.size,
        }

        if query.sort_by:
            body['sort'] = [{query.sort_by: {'order': query.sort_order}}]

        result = await self.es.search(index='alerts', body=body)

        hits = result['hits']['hits']
        return [self._hit_to_alert(hit) for hit in hits]

    async def bulk_add(self, alerts: list[Alert]) -> None:
        actions = [
            {
                '_op_type': 'index',
                '_index': 'alerts',
                '_id': str(alert.id),
                '_source': alert_to_document(alert),
            }
            for alert in alerts
        ]
        await async_bulk(self.es, actions)

    async def delete(self, alert: Alert) -> None:
        await self.es.delete(index='alerts', id=str(alert.id), ignore_unavailable=True)

    async def update(self, alert: Alert) -> None:
        doc = alert_to_document(alert)
        await self.es.update(index='alerts', id=str(alert.id), doc=doc)

    @staticmethod
    def _hit_to_alert(hit: dict[str, Any]) -> Alert:
        data = hit['_source']
        data['id'] = AlertId(hit['_id'])
        data['event_id'] = SensorEventId(data['event_id'])
        data['device_id'] = DeviceId(data['device_id'])
        del data['severity_label']
        return Alert(**data)
