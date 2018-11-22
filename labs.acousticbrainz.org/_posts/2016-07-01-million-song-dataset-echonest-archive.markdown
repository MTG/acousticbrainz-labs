---
layout: post
title:  "Million Song Dataset Echo Nest mapping archive"
date:   2016-07-01 00:00:00
categories:  mappings
---

The [Million Song Dataset](http://labrosa.ee.columbia.edu/millionsong/) was
released in collaboration with [The Echo Nest](http://the.echonest.com), and
uses Echo Nest identifiers
to refer to each track. While the metadata that comes with the dataset includes
names of tracks and artists, in June 2016, the Echo Nest shut down their
API, leaving no service available which understood the IDs.

A valuable service provided by the Echo Nest API was Rosetta Stone, a
mapping between Echo Nest IDs and IDs from other music services.

We performed a lookup of all Echo Nest Song IDs present in the Million
Song Dataset, obtaining mappings to IDs of other services where
available.

## Method

We used the `/song/profile` endpoint for each Song ID. The queries included
the following rosetta stone buckets:

    id:7digital-US, id:7digital-AU, id:7digital-UK, id:facebook, id:fma, id:twitter, id:spotify-WW, id:seatwave, id:lyricfind-US, id:jambase, id:musixmatch-WW, id:seatgeek, id:openaura, id:spotify, id:spotify-WW, id:tumblr, id:musicbrainz, id:discogs, id:eventful, id:songkick, id:songmeanings, id:whosampled

## Data

We provide the following file

 * [`millionsongdataset_echonest.tar.bz2`](ftp://ftp.acousticbrainz.org/pub/acousticbrainz/acousticbrainz-labs/download/msdrosetta/millionsongdataset_echonest.tar.bz2) (461M): The result of looking up `/song/profile` in the Echo Nest API for all Song IDs in the Million Song Dataset.

## File contents and accuracy

Note that the track list in these files does not include the Million Song
Dataset track ID. Use the [MSD SQLite database file](http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset) to map Song IDs to Track IDs.

The archive has JSON files containing the results of looking up each
individual Song ID. The files are named in directories based on the 2nd
and 3rd letters of the Song ID, i.e., `XX/SOXXnnnnnnnnnn.json`
We have not validated any of the data in the archive.

Here is a truncated and annotated version of the file `CW/SOCWJDB12A58A776AF.json`:
{% highlight json %}
{
  "response": {
    "status": {
      "version": "4.2",
      "code": 0,
      "message": "Success"
    },
    "songs": [ // Only one song per file
      {
        "artist_foreign_ids": [
          // IDs on other services for this Artist. This section is duplicated in all JSON
          // files representing songs with the same Artist ID.
          {
            "foreign_id": "facebook:artist:59520506051",
            "catalog": "facebook"
          },
          {
            "foreign_id": "musicbrainz:artist:db92a151-1ac2-438b-bc43-b82e149ddd50",
            "catalog": "musicbrainz"
          },
          {
            "foreign_id": "discogs:artist:72872",
            "catalog": "discogs"
          },
          ... // More Artist IDs
        ],
        "id": "SOBVVPR1373FF8B516", // Note that the Song ID in the response may be different to the request/filename
        "title": "Never Gonna Give You Up",
        "artist_name": "Rick Astley",
        "foreign_ids": [
          {
            "foreign_id": "musixmatch-WW:song:14679007",
            "catalog": "musixmatch-WW"
          },
          {
            "foreign_id": "musixmatch-WW:song:15195315",
            "catalog": "musixmatch-WW"
          },
          ... // More Foreign IDs
        ],
        "tracks": [
          // Mappings to IDs in other services. If a track appears on another service more than once it may appear
          // multiple times here, with different Track IDs. The MSD Track ID will not appear in this list.
          {
            "album_name": "Whenever You Need Somebody",
            "foreign_id": "7digital-UK:track:3107215",
            "release_image": "http://artwork-cdn.7static.com/static/img/sleeveart/00/002/790/0000279033_200.jpg",
            "catalog": "7digital-UK",
            "id": "TRCAZUD12E5B35943B",
            "album_type": "unknown",
            "album_date": "1987-10-01",
            "foreign_release_id": "7digital-UK:release:279033",
            "preview_url": "http://previews.7digital.com/clip/3107215"
          },
          {
            "album_name": "Whenever You Need Somebody",
            "foreign_id": "spotify:track:4uLU6hMCjMI75M1A2tKUQC",
            "catalog": "spotify",
            "id": "TRIOLQS144D1655A22",
            "album_type": "unknown",
            "album_date": "1987-10-01",
            "foreign_release_id": "spotify:album:6N9PS4QXF1D0OWPk0Sxtb4"
          },
          {
            "album_name": "Whenever You Need Somebody",
            "foreign_id": "spotify:track:7GhIk7Il098yCjg4BQjzvb",
            "catalog": "spotify",
            "id": "TRXHFOZ144D1D145D6",
            "album_type": "unknown",
            "album_date": "1987-10-01",
            "foreign_release_id": "spotify:album:6XhjNHCyCDyyGJRM5mg40G"
          },
          {
            "album_name": "Now That’s What I Call Music! 1987",
            "foreign_id": "spotify:track:32A0G3IqWI43wXzY5WZI5X",
            "catalog": "spotify",
            "id": "TRQVKVZ147F7196983",
            "album_type": "other",
            "album_date": "1993-08-23",
            "foreign_release_id": "spotify:album:4ZTvxAlhcV9JzMz4vHMW95"
          },
          {
            "foreign_id": "musicbrainz:track:0117e142-bcd7-4956-9dde-c450839988a1",
            "foreign_release_id": "musicbrainz:release:2fa1f6aa-bba7-4877-9442-7879c7f05c74",
            "catalog": "musicbrainz",
            "id": "TRLGGVH13B7B548EFD"
          },
          {
            "foreign_id": "musicbrainz:track:01241823-25d2-4bcb-9179-fac2a254c42c",
            "foreign_release_id": "musicbrainz:release:0c3b8dfe-1d31-4f69-abbf-5acd6e29d2cb",
            "catalog": "musicbrainz",
            "id": "TRCJMFG13B7B54AAD1"
          },
          {
            "foreign_id": "discogs:track:864861#19",
            "foreign_release_id": "discogs:release:864861",
            "catalog": "discogs",
            "id": "TRAOFGZ13A5C01365C"
          },
          ... // More Tracks
        ],
        "artist_id": "ARWPYQI1187FB4D55A"
      }
    ]
  }
}
{% endhighlight %}
