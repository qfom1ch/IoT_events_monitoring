ALERT_INDEX_MAPPING = {
    'mappings': {
        'properties': {
            'id': {'type': 'keyword'},
            'event_id': {'type': 'keyword'},
            'device_id': {'type': 'keyword'},
            'message': {'type': 'text'},
            'severity': {'type': 'keyword'},
            'severity_label': {'type': 'keyword'},
            'created_at': {'type': 'date'},
        }
    }
}
