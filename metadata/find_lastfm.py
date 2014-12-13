import threader
import argparse
import json
import lfm_scraper
import time

class LastFm(threader.ComputationThread):
    """
        This thread gets tag and metadata from lastfm
    """

    tablename = "lastfm"

    def _calculate(self):
        """
           Invoke essentia high level extractor and return its JSON output
        """
        lowlevel = json.loads(self.ll_data)
        tags = lowlevel["metadata"]["tags"]
        mbid = tags.get("musicbrainz_recordingid", [None])[0]
        artist = tags.get("artist", [None])[0]
        track = tags.get("title", [None])[0]

        d, msg = lfm_scraper.getTopTags(mbid, artist, track)
        self.data = d
        time.sleep(1)

    @classmethod
    def write_to_database(cls, conn, mbid, data):
        cur = conn.cursor()
        data = json.dumps(data)
        cur.execute("""INSERT INTO lastfm (mbid, data)
                            VALUES (%s, %s)""", (mbid, data))
        conn.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract high level data from lowlevel data')
    parser.add_argument("-t", "--threads", help="Number of threads to start", default=threader.DEFAULT_NUM_THREADS, type=int)
    args = parser.parse_args()
    threader.main(args.threads, LastFm)
