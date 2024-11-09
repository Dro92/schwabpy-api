import logging.config
import logging.handlers
import json
import datetime as dt
import copy
import pytz

# https://docs.python.org/3/library/logging.config.html#dictionary-schema-details
LOGGING_MODULE_VERSION = 1

# https://docs.python.org/3.10/library/logging.html#logrecord-attributes
LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "message",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


class LogJsonFormatter(logging.Formatter):
    def __init__(self, *, fmt_keys: dict[str, str] | None = None):
        """"""
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        """"""
        message = self._process_log_dict(record)
        return json.dumps(message, default=str)

    def _get_Current_time():
        return dt.datetime.now(pytz.timezone("UTC")).astimezone().tzinfo

    def _process_log_dict(self, record: logging.LogRecord):
        """
        Return:
            Serialized JSON string.
        """

        # TODO: Re-write so msg is not mandatory
        always_include_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.now().isoformat(),
        }

        # If message is included
        # if record.getMessage():
        #     always_include_fields["message"] = record.getMessage()

        # If exception record is received
        if record.exc_info is not None:
            always_include_fields["exc_info"] = self.formatException(record.exc_info)

        # If stack frame record is received
        if record.stack_info is not None:
            always_include_fields["stack_info"] = self.formatStack(record.stack_info)

        # TODO: This needs re-work to suppress None values
        # Iterate over key, values. If key is NOT in included fields, add k,v, else update value
        message = {
            key: (
                msg_val
                if (msg_val := always_include_fields.pop(val, None))
                else getattr(record, val)
            )
            for key, val in self.fmt_keys.items()
        }

        message.update(always_include_fields)

        # Protect built in fields
        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS and val is not None:
                message[key] = val

        return message


DEFAULT_LOG_CONFIG = {
    "version": LOGGING_MODULE_VERSION,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": globals().get("LogJsonFormatter"),
            "fmt_keys": {
                "level": "levelname",
                "message": "message",
                "timestamp": "timestamp",
                "module": "module",
                "func": "funcName",
                "thread": "thread",
                "threadName": "threadName",
            },
        }
    },
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "json",
            "stream": "ext://sys.stderr",
        },
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
        "fileout": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "json",
            "filename": "app.log",
            "maxBytes": 50000000,  # 50MB max
            "backupCount": 2,  # Two file max
        },
    },
    "loggers": {"json": {"level": "INFO", "handlers": ["stdout"]}},
}


def setup_logging(custom_config: dict | None = None) -> logging:
    """"""

    log_config = copy.deepcopy(DEFAULT_LOG_CONFIG)
    # Allow user to provide their own config
    if custom_config is not None:
        log_config.update(custom_config)

    logging.config.dictConfig(log_config)
    return log_config


logger = logging.getLogger("json")
setup_logging()
