import eyed3
import glob
import os
import pandas as pd
import count_map as cm 


def get_taglist(mypath):

	files = glob.glob(mypath + '/**/*.mp3', recursive=True)

	taglist = []
	for filename in files: 

	    audfile = eyed3.load(filename)
	    tags = []
	    tags.append(filename.replace(mypath, '')[1:])
	    tags.append(audfile.tag.title)
	    tags.append(audfile.tag.artist)
	    tags.append(audfile.tag.album)

	    ids = list(audfile.tag.unique_file_ids)

	    for i in ids:
	        if i.owner_id.decode('utf-8') == 'http://musicbrainz.org':
	            d = i.data.decode('utf-8').split('\0')
	            tags.append(d[-1])

	            #Had to modify function to make it return count_mapping
	            if cm.get_count_for_id_chunk([d[-1]], {})[d[-1]] != None:
	            	tags.append('yes')
	            
	    taglist.append(tags)

	df = pd.DataFrame(taglist, columns=['filename', 'title', 'artist', 'album', 'mbid', 'is_in_acoustic_brainz'])
	df.to_csv('genre_rosamerica.csv', index=False)

	return df


def get_dataset_for_upload(mypath):
	
	files = glob.glob(mypath + '/**/*.mp3', recursive=True)

	ds = []
	for filename in files: 

	    audfile = eyed3.load(filename)
	    ids = list(audfile.tag.unique_file_ids)

	    for i in ids:
	        if i.owner_id.decode('utf-8') == 'http://musicbrainz.org':
	            d = i.data.decode('utf-8').split('\0')

	            gen = filename.split('/')[-2]
	            ds.append([d[-1], gen])

	df = pd.DataFrame(ds)
	df.to_csv('gr_dataset.csv', index=False)

	return df


def get_files_not_in_ab(mypath, df):

	#We drop the ones without mbid
	df2 = df.dropna(subset=['mbid'])  

	fn = mypath + '/' + df2['filename']
	ab = df2['is_in_acoustic_brainz']

	sub = []
	for i, el in enumerate(ab):
		if el == None: 
			sub.append(list(fn)[i])

	with open('filelist.txt', 'w') as f:
	    for item in sub: 
	        f.write(item + ' ')

	return


def main(mypath):

	df1 = get_taglist(mypath)
	get_files_not_in_ab(mypath, df1)
	df2 = get_dataset_for_upload(mypath)

	return 


if __name__ == "__main__":
	mypath = '/home/sara/Desktop/genre_rosamerica/audio/mp3'
	main(mypath)