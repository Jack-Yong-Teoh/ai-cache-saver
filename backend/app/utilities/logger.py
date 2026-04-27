import logging
import sys
from datetime import datetime
from sqlalchemy import log as sqlalchemy_log
from pythonjsonlogger import jsonlogger
from app.utilities.contextvar import contextvar_correlation_id, contextvar_endpoint


class LogFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            log_record["timestamp"] = datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        if log_record.get("pathname") and log_record.get("lineno"):
            log_record["file"] = f"{log_record['pathname']}:{log_record['lineno']}"
            for x in ["pathname", "lineno"]:
                del log_record[x]

        context_variables = {
            "correlation_id": contextvar_correlation_id,
            "endpoint": contextvar_endpoint,
        }
        for k, v in context_variables.items():
            value = v.get()
            if value:
                log_record[k] = value


logger = logging.getLogger()
logHandler = logging.StreamHandler(sys.stdout)
formatter = LogFormatter("%(level) %(timestamp) %(message) %(pathname)s %(lineno)d")
logHandler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(logHandler)
logging.getLogger("pika").propagate = False
logging.getLogger("boto3").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("s3transfer").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("multipart").setLevel(logging.ERROR)
# pylint: disable-next=protected-access
sqlalchemy_log._add_default_handler = lambda x: None
