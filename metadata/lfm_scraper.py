import csv
import lastfmapi
import json
import socket
from optparse import OptionParser

SYSTEM_NAME = socket.gethostname()

LAST_FM_API_KEYS = {'machine-name': 'lastfm-api-key'}
API_KEY = "61463d0cba86a3c0fbbf7ba0a696cec1"
api = lastfmapi.LastFmApi(API_KEY)

def getTopTags(mbid, artistname, trackname):
    try:
        data = api.track_getTopTags(mbid=mbid)
        message = ["mbid"]
        return data, message
    except Exception as ex:
        message = ex.args
        if len(message) > 0:
            if message[0] == "Track not found" and artistname and trackname:
                try:
                    data = api.track_getTopTags(track=trackname, artist=artistname)
                    message = ["name"]
                    return data, message
                except:
                    pass
        else:
            message = ["IndexError: tuple index out of range"]
    return None, message

def topTagswriter(inputFile, outputFolder, outputLogfile):
    """
    Writes LastFM's track.getTopTags to single JSON files
    """

    idx = 0
    with open(inputFile, 'rb') as csvinput:
        with open(outputLogfile, 'wb') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)
            for row in reader:
                idx += 1

                data, message = getTopTags(row[0], row[1], row[2])

                if data:
                    with open(outputFolder + mbid + '.json', 'w') as outfile:
                        json.dump(data, outfile)
                line = []
                line.append(row[0])
                line.append(message[0])
                print idx, line
                writer.writerow(line)


def getInfowriter(inputFile, outputFolder, outputLogfile):
    """
    Writes LastFM's track.getTopTags to single JSON files
    """

    api = lastfmapi.LastFmApi(LAST_FM_API_KEYS[SYSTEM_NAME])
    idx = 0
    with open(inputFile, 'rb') as csvinput:
        with open(outputLogfile, 'wb') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)
            for row in reader:
                idx += 1
                mbid = row[0]
                try:
                    data = api.track_getInfo(mbid=mbid)
                    message = ["mbid"]
                    with open(outputFolder + mbid + '.json', 'w') as outfile:
                        json.dump(data, outfile)
                except Exception as ex:
                    message = ex.args
                    if len(message) > 0:
                        if message[0] == "Track not found":
                            artistname = row[1]
                            trackname = row[2]
                            try:
                                data = api.track_getInfo(track=trackname, artist=artistname)
                                message = ["name"]
                                with open(outputFolder + mbid + '.json', 'w') as outfile:
                                    json.dump(data, outfile)
                            except:
                                pass
                    else:
                        message = ["IndexError: tuple index out of range"]
                line = []
                line.append(row[0])
                line.append(message[0])
                print idx, line
                writer.writerow(line)


if __name__ == "__main__":
    usage = "usage: %prog [options] inputFile outputFolder outputLogfile"
    opts = OptionParser(usage=usage)
    options, args = opts.parse_args()

    # topTagswriter(args[0], args[1], args[2])
    getInfowriter(args[0], args[1], args[2])
