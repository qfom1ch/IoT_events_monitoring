from src.domain.alerts.entities.alert import Alert
from src.domain.alerts.interfaces.alert_repo import AlertRepository
from src.domain.alerts.value_objects.alert_id import AlertId
from src.infrastructure.mongodb.alerts.orm import AlertDB


class MongoAlertRepository(AlertRepository):
    async def find_by_id(self, alert_id: AlertId) -> Alert | None:
        if alert_db := await AlertDB.get(alert_id.value):
            alert: Alert = alert_db.to_domain()
            return alert
        return None

    async def save(self, alert: Alert) -> None:
        alert_db = AlertDB.from_domain(alert)
        await alert_db.insert()
