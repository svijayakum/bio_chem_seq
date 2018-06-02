#!/usr/bin/python
import logging


class Logger(object):
    def get_logger(self, name=__name__,
                   log_format='%(asctime)s [%(levelname)s][%(name)s] %(message)s',
                   log_level='ERROR',
                   log_handler='stream',
                   log_dir='./service.log',
                   ):

        log_levels = {
            'CRITICAL': logging.CRITICAL,
            'ERROR': logging.ERROR,
            'WARNING': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'NOTSET': logging.NOTSET,
        }

        assert log_level in log_levels.keys()

        logger = logging.getLogger(name)
        logger.setLevel(log_levels[log_level])
        logger.handlers = []

        formatter = logging.Formatter(log_format)

        if log_handler == 'file':
            file_handler = logging.FileHandler(log_dir)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        if log_handler == 'stream':
            logger.addHandler(stream_handler)

        # Fallthrough console logger
        if not logger.handlers:
            logger.addHandler(stream_handler)

        return logger
