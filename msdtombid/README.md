## Million Song Dataset to AcousticBrainz mapping

### Requirements

You need the following additional python packages:

    requests requests_cache

Use `pip install -r requirements` to install them


You also need the MSD metadata file, which you can download from
http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset
under Additional Files,
* 8. SQLite database containing most metadata about each track


The matcher uses the MusicBrainz search server to perform matches and
find a recording matching the given artist details.
You need to set up a local Musicbrainz database and search server,
as the 1 query per second ratelimit on musicbrainz.org makes querying
1 million items prohibitive. Follow the instructions at
http://wiki.musicbrainz.org/Development/Search_server_setup

You only need to build the `recording` indexes in order to run this.

Alternatively, you can download a complete MusicBrainz virtual machine and
build indexes on that:
https://wiki.musicbrainz.org/MusicBrainz_Server/Setup

Set `SEARCHSERVER_URL` at the top of the source file to the address of your
search server.

### Running

The script has 3 modes:

**match**: Match items in MSD to MusicBrainz IDs

    python msdtombid.py match track_metadata.db matches.json

This reads items in `track_metadata.db`, and looks them up in a MusicBrainz search server.
It writes to the output file (`matches.json`) every 1000 results. Webservice results are
cached with `requests_cache`, so you can stop and re-run the command and cached results
will not be looked up in the API. Remove `msdtombidcache.sqlite` to clear the cache.

**filter**: Remove items that are not in AcousticBrainz

    python msdtombid.py filter matches.json uniq-ab-ids.csv filter-matches.json

Filter `matches.json` to contain only MBIDs which are in the file `uniq-ab-ids.csv` (one
mbid per line)

**csv**: Convert a `matches.json` file to a simplified csv file

    python msdtombid.py csv matches.json matches.csv

The output file will contain the following columns: `msdid, mbid, title, artist`.
If a MSD track matches more than one mbid, there will be multiple lines in the output file
for each mbid. If a recording has more than one artist they will be joined by " and "
