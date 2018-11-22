---
layout: post
title:  "Million Song Dataset to AcousticBrainz mapping"
date:   2016-01-04 15:35:42
categories:  mappings
---

A well known dataset in MIR is the [Million Song Dataset](http://labrosa.ee.columbia.edu/millionsong/).
It is useful to be able compare results between this dataset and AcousticBrainz, and so we provide
a mapping of IDs between the two datasets.

We currently have a mapping for about 250,000 MSD IDs, resulting in 370,000 matches (because a
MSD ID may map to more than one MusicBrainz ID).


## Source code

The code to recreate the data files is available on github:
[https://github.com/MTG/acousticbrainz-labs/tree/master/msdtombid](https://github.com/MTG/acousticbrainz-labs/tree/master/msdtombid)
See the README.md file in that directory for more information on how to run it.

## Files

We provide the following files containing the data of this mapping

 * [`msd-mbid-2016-01-abz-mbids.csv.bz2`](ftp://ftp.acousticbrainz.org/pub/acousticbrainz/acousticbrainz-labs/download/msdtombid/msd-mbid-2016-01-abz-mbids.csv.bz2) (33M): A unique list of MusicBrainz IDs present in AcousticBrainz at the time of the matching
 * [`msd-mbid-2016-01-results.json.bz2`](ftp://ftp.acousticbrainz.org/pub/acousticbrainz/acousticbrainz-labs/download/msdtombid/msd-mbid-2016-01-results.json.bz2) (195M): A mapping of MSD IDs and metadata to Recordings in MusicBrainz
 * [`msd-mbid-2016-01-results-ab.json.bz2`](ftp://ftp.acousticbrainz.org/pub/acousticbrainz/acousticbrainz-labs/download/msdtombid/msd-mbid-2016-01-results-ab.json.bz2) (60M): The same mapping file, containing MBIDs only present in AcousticBrainz (filtered with the first file)
 * [`msd-mbid-2016-01-results-ab.csv.bz2`](ftp://ftp.acousticbrainz.org/pub/acousticbrainz/acousticbrainz-labs/download/msdtombid/msd-mbid-2016-01-results-ab.csv.bz2) (13M): The AB mapping file in CSV format, with simplified metadata

## File format

The json mapping files have the following format:

{% highlight json %}
{
  "query": { // MSD metadata used for the query
    "song_id": "SOTUGDX12A8C13E5F7",
    "title": "Aground",
    "artist_name": "Fresh Moods",
    "track_id": "TRMRLVN128F42AA35E",
    "release": "Exhale",
    "duration": "377.02485",
    "artist_mbid": "cba5dbef-14f8-47a7-8632-a63e7a9738e2"
  },
  "match": [ // A list of all results from MusicBrainz which match on artist id and title
    {
      "length": 375000,
      "title": "Aground",
      "id": "eb301e57-5c6d-49a4-bb0d-2d963ca5a59b",
      "releases": [ // Releases on which this recording appears. Could be more than 1
        {
          "id": "24e38551-44ab-4aed-81c6-b60447dbfd0d",
          "title": "Campari Lounge II"
        }
      ],
      "artists": [ // Artists from MusicBrainz. Could be more than 1
        {
          "id": "cba5dbef-14f8-47a7-8632-a63e7a9738e2",
          "name": "Fresh Moods"
        }
      ]
    },
    {
      "length": 380026,
      "title": "Aground",
      "id": "47ce77c9-9296-4bc3-a878-7390a3303e0c",
      "releases": [
        {
          "id": "6ca97f9c-b764-4c98-b512-3ddf6e51db79",
          "title": "Exhale"
        }
      ],
      "artists": [
        {
          "id": "cba5dbef-14f8-47a7-8632-a63e7a9738e2",
          "name": "Fresh Moods"
        }
      ]
    }, //... More matches
  ],
  "matchtypes": { // Some data about how the MusicBrainz data matches the MSD data
    "duration": "withindur",
    "release": "",
    "type": "exact"
  }
}
{% endhighlight %}
