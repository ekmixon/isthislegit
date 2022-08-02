# Memcache helper library
# Credit @cczub

from google.appengine.api import memcache
import json
import logging

MAX_VALUE_SIZE = 10 ** 6

# one hour
TIMEOUT = 60 * 60
# 5 minutes per view cache
PAGE_TIMEOUT = 60 * 5


def _split_value(value):
    parts = []

    if isinstance(value, str):
        pass
    elif isinstance(value, unicode):
        value = value.encode('utf-8')

    while len(value) > MAX_VALUE_SIZE:
        # need to split
        parts.append(value[:MAX_VALUE_SIZE])
        value = value[MAX_VALUE_SIZE:]
    parts.append(value)

    return parts


def delete(key=None):
    if parts_count := memcache.get(key=f'{key}_parts'):
        for i in xrange(parts_count):
            memcache.delete(key='%s%d' % (key, i))

    memcache.delete(key=key)
    memcache.delete(key=f'{key}_parts')


def set(key=None, value=None, time=TIMEOUT):
    parts = _split_value(json.dumps(value))
    memcache.set(key=f'{key}_parts', value=len(parts), time=time)
    for i, part in enumerate(parts):
        logging.debug("Setting %s%d" % (key, i))
        memcache.set(key='%s%d' % (key, i), value=part, time=time)


def get(key):
    if not (parts_count := memcache.get(key=f'{key}_parts')):
        return memcache.get(key)
    chunk = ''
    for i in xrange(parts_count):
        logging.debug("Fetching %s%d" % (key, i))
        chunk += str(memcache.get(key='%s%d' % (key, i)))
    return json.loads(chunk)
