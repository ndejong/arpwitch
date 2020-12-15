
import json
import datetime

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'
# TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S %Z%z'


def timestamp():
    return datetime.datetime.utcnow().strftime(TIMESTAMP_FORMAT)


def out(data, indent=2, flush=False):
    if type(data) is str:
        print(data)
    else:
        if indent > 0:
            print(json.dumps(data, indent=indent), flush=flush)
        else:
            print(json.dumps(data, indent=indent, separators=(',', ':')).replace('\n',''), flush=flush)
