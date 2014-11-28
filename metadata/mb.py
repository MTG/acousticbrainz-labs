import musicbrainzngs
from functools import wraps
import json
import redis

rconn = redis.StrictRedis(host="localhost")
musicbrainzngs.set_hostname("musicbrainz.s.upf.edu")
musicbrainzngs.set_rate_limit(False)
musicbrainzngs.set_useragent("test", "test")

def cache(f):
    @wraps(f)
    def inner(*args, **kwargs):
        # TODO: understand args and kwargs
        # -- args[0] is mbid
        key = "%s:%s" % (f.__name__, args[0])
        val = rconn.get(key)
        if not val:
            ret = f(*args, **kwargs)
            val = json.dumps(ret)
            rconn.set(key, val)
        else:
            ret = json.loads(val)
        return ret
    return inner

@cache
def get_recording(mbid):
    try:
        rec = musicbrainzngs.get_recording_by_id(mbid, includes=["releases", "artists"])
        return rec["recording"]
    except musicbrainzngs.ResponseError:
        return {}

@cache
def get_release(mbid):
    try:
        rel = musicbrainzngs.get_release_by_id(mbid, includes=["release-groups"])
        return rel["release"]
    except musicbrainzngs.ResponseError:
        return {}
