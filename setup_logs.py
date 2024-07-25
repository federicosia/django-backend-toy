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
        if not kwargs.get("host") or not kwargs.get("port"):
            raise Exception("Host and port are mandatory parameters")
        super().__init__()
        self.sender = LogStashLogSender(kwargs.get("host"), kwargs.get("port"))

    def emit(self, record) -> None:
        self.sender.writeLog(record)


class LogStashLogSender:
    def __init__(self, host, port):
        self.UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.first_error = 0

    def writeLog(self, record: logging.LogRecord):
        try:
            self.UDPsocket.sendto(
                bytes(
                    datetime.now().replace(microsecond=0).isoformat()
                    + " - "
                    + record.levelname
                    + " - "
                    + record.funcName
                    + " - "
                    + record.msg,
                    "utf-8",
                ),
                (self.host, self.port),
            )
        except Exception as e:
            if self.first_error == 0:
                print(
                    f"Missing {self.host}:{self.port} to send UDP packages -> {e}. "
                    f"\nN.B: if running in a CI/CD it is normal..."
                )
                self.first_error += 1
