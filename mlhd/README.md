# MLHD
This folder contains a series of scripts used to obtain data from recordings in the [MLHD](http://ddmal.music.mcgill.ca/research/musiclisteninghistoriesdataset) that can also be found in AcousticBrainz.

## Usage of scripts
The scripts are supposed to be run in a certain order. You can skip a step if you already have the required files for the next step.

## Step 1: Getting a list of IDs
The script to use in this step is `id_list.py`, which gets a list of MBIDs to do the following lookup. 

It outputs a file called `mbid_list.txt`, which is a list of all the different MBIDs. 

### Required files
To be able to get the data it is necessary to have the following files: 
- `MLHD_recording_mbids.txt`: contains a list of all the MBIDs that correspond to the different recordings in the MLHD
- `recording_gid_redirect.csv`: contains a mapping between MBIDS. This is because one song can be submitted multiple times and thus have multiple MBIDs. With  this mapping file we make sure we are using all the possible MBIDs for each recording in the MLHD when doing the 
### Alternate files
If you have similar files and you want to use them you can change the name in the script. Go to:
```python
if __name__ == "__main__":

    mbid_file = 'MLHD_recording_mbids.txt'
    gid_map_file = 'recording_gid_redirect.csv'
    id_list = main(mbid_file, gid_map_file)
```
and just change the values in `mbid_file` and `gid_map_file` to your desired id or mapping files.

## Step 2: Getting the count for each ID
The script to use in this step is `count_map.py`, which gets a count of how many submissions of that MBID are in AcousticBrainz. If the recording doesn't exist in AcousticBrainz, the count value will be null. 

It outputs a file called `id_counts.json`.

### Required Files
To be able to get the data it is necessary to have the following file: 
- `mbid_list.txt`: contains a list of all the mbids to do the count lookup. It is the output file of the 1st script. 
### Alternate Files
You can use your own list of MBIDs if you already have it, you just have to change it in the script. Go to:
```python
if __name__ == "__main__":

    id_list_file = 'mbid_list.txt'
    count_mapping = main(id_list_file)
```
and change the `id_list_file` value to your file name. 

## Step 3: Get low-level data
The script to use in this step is `low_level.py`, which gets low-level data for all the IDs. It gets data for as many submissions there are for each recording, that is why the count is needed. It only gets the data if the count is not null. 

It outputs a file for each different ID, having all the different submissions inside. 
#### Output format
If we have the following MBID: `1f5cc450-7ed3-4329-9f47-2a97b8cbd58a` then it will be split like this: `1f/5c/c450-7ed3-4329-9f47-2a97b8cbd58a_lowlevel.json`. It splits the 1st and 2nd pair of characters from the name and puts it as directories and then the rest of the id as the file name. This way we can group MBIDs that start with the same values and it makes searching for files a lot easier. 

### Required Files
To be able to get the data it is necessary to have the following file:
- `ìd_counts.json`: contains a mapping of MBIDs and the count of submissions that are in AcousticBrainz for each ID. It is the output file of the 2nd script. 
### Alternate Files
You can use your own count mapping file if you have it. Go to: 
```python
if __name__ == "__main__":

    counts_file = 'id_counts.json'
    main(counts_file)
```
and change the value of `counts_file` to the name of your file. 
