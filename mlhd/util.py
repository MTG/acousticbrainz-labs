import os
import errno
import time
import datetime


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def stats(done, total, starttime):
    nowtime = time.time()
    position = done*1.0 / total
    duration = round(nowtime - starttime)
    durdelta = datetime.timedelta(seconds=duration)
    remaining = round((duration / position) - duration)
    remdelta = datetime.timedelta(seconds=remaining)

    return str(durdelta), str(remdelta)
