# MLHD
This folder contains scripts to download AcousticBrainz features for recordings that
are in the [MLHD](http://ddmal.music.mcgill.ca/research/musiclisteninghistoriesdataset)
that can also be found in AcousticBrainz.

## Usage of scripts
Run each script in order

## Step 1: Getting a list of IDs
`id_list.py` takes a list of MBIDs and a copy of the MusicBrainz `recording_gid_redirect` table
to make a list of all possible MBIDs that could represent a given MBID.

For example, given a list of mbids:

    a
    b

and a mapping

    a,1
    a,2
    b,3

This script will return a list:

    a,b,1,2,3



## Step 2: Getting the count for each ID
`mbid_counts.py` gets a count of how many submissions of a list of MBIDs are in AcousticBrainz.
If the recording doesn't exist in AcousticBrainz, the count value will be null.

It takes as an input the MBID list from the previous step.

It outputs a json file containing a mapping of MBID: count

## Step 3: Get low-level data
`download_lowlevel.py` downloads all low-level data for each of the MBIDs in the output file from the
previous step.
In the given `dest_dir` destination, it will create two subfolders and file for each submission:

    1f5cc450-7ed3-4329-9f47-2a97b8cbd58a -> 1f/5c/c450-7ed3-4329-9f47-2a97b8cbd58a-n.json

where `-n` is the duplicate submission number.
