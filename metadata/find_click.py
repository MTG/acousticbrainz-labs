#!/usr/bin/env python

import sys
sys.path.append("../tempoStability")

import argparse
import threader
import stableTempoFast
import json

class ClickTrack(threader.ComputationThread):
    """
        This thread calculates tempo stability of a track
    """
    tablename = "tempo"
    def _calculate(self):
        lowlevel = json.loads(self.ll_data)
        try:
            self.data = stableTempoFast.processData(lowlevel, thres=2.0, thresRamp=20.0, perc=80.0, tstep=0.5)
        except:
            self.data = {}

    @classmethod
    def write_to_database(cls, conn, mbid, data):
        cur = conn.cursor()
        data = json.dumps(data)
        cur.execute("""INSERT INTO tempo (mbid, data)
                            VALUES (%s, %s)""", (mbid, data))
        conn.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract high level data from lowlevel data')
    parser.add_argument("-t", "--threads", help="Number of threads to start", default=threader.DEFAULT_NUM_THREADS, type=int)
    args = parser.parse_args()
    threader.main(args.threads, ClickTrack)

