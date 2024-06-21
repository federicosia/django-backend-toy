import os.path
import socket
from datetime import datetime

import yaml
import logging
import logging.config


def setup_logging(default_level=logging.INFO):
    path = os.path.join(os.getcwd(), "logging.yml")
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print("Error in Logging Configuration. Using default configs")
                logging.basicConfig(level=default_level)
            finally:
                return logging
    else:
        logging.basicConfig(level=default_level)
        print("Failed to load configuration file. Using default configs")
        return logging


class LogstashDatagramHandler(logging.Handler):
    def __init__(self, **kwargs):
        super().__init__()
        self.sender = LogStashLogSender(kwargs.get("host"), kwargs.get("port"))

    def emit(self, record) -> None:
        self.sender.writeLog(record)


class LogStashLogSender:
    def __init__(self, host, port):
        self.UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port

    def writeLog(self, record: logging.LogRecord):
        print(f"send log to {self.host}:{self.port}")
        self.UDPsocket.sendto(
            bytes(
                datetime.now().replace(microsecond=0).isoformat()
                + " - "
                + record.levelname
                + " - "
                + record.msg,
                "utf-8",
            ),
            (self.host, self.port),
        )
