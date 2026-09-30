import logging


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return True


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s "
            "- [request_id=%(request_id)s] - %(message)s"
        )

        handler.setFormatter(formatter)
        handler.addFilter(RequestIdFilter())

        logger.addHandler(handler)

        logger.setLevel(logging.INFO)

    return logger