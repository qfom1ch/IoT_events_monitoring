from src.domain.alerts.entities.alert import Alert


def alert_to_document(alert: Alert) -> dict:
    severity_map = {1: 'low', 2: 'medium', 3: 'high', 4: 'critical'}
    return {
        'id': str(alert.id),
        'event_id': str(alert.event_id),
        'device_id': str(alert.device_id),
        'message': alert.message,
        'severity': alert.severity.value,
        'severity_label': severity_map[alert.severity.value],
        'created_at': alert.created_at.isoformat(),
    }
