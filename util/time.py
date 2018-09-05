from datetime import datetime

epoch = datetime.utcfromtimestamp(0)
format_str = '%Y-%m-%dT%H:%M:%S.%fZ'

def parse_datetime(s):
    return datetime.strptime(s, format_str)

def to_epoch_ms(dt):
    return int((dt - epoch).total_seconds() * 1000)