import json
import logging
from datetime import datetime
from pathlib import Path


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            'timestamp': datetime.utcfromtimestamp(record.created).isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'msg': record.getMessage(),
        }

        if hasattr(record, 'extra') and isinstance(record.extra, dict):
            log_entry.update(record.extra)

        if record.exc_info:
            log_entry['exc_info'] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False, default=str)


def setup_logging(log_dir: str = 'logs', log_file: str = 'app.log') -> logging.Logger:
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    log_file_path = log_path / log_file

    logger = logging.getLogger('IoT_events_monitoring')
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(JSONFormatter())
    file_handler.set_name('file')
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        fmt='[{asctime}] {levelname} {name}: {message}', style='{', datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    console_handler.set_name('console')
    logger.addHandler(console_handler)

    return logger
