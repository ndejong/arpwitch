
import os
import json

from arpwitch import __version__ as VERSION
from arpwitch.ArpWitch import timestamp
from arpwitch.ArpWitch import logger


class ArpWitchDataFile:

    @staticmethod
    def read(filename):
        logger.debug('ArpWitchDataFile.read(filename={})'.format(filename))

        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
            logger.debug('ArpWitchDataFile.read() - data file loaded')
        else:
            logger.warning('ArpWitchDataFile.read() - no existing data file found')
            data = {
                'meta':{
                    'arpwitch': VERSION,
                    'starts': 0,
                    'ts_first': timestamp(),
                    'ts_last': timestamp(),
                    'hw_count': 0,
                    'ip_count': 0,
                },
                'ip': {},
                'hw': {},
            }

        for meta_field in data['meta']:
            logger.debug('{}: {}'.format(meta_field, data['meta'][meta_field]))

        return data

    @staticmethod
    def write(filename, data):
        logger.debug('ArpWitchDataFile.write(filename={}, data=<data>)'.format(filename))

        with open(filename, 'w') as f:
            json.dump(data, f)

        logger.debug('ArpWitchDataFile.write() - datafile written')
