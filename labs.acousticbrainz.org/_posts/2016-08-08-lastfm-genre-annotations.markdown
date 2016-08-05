---
layout: post
title:  "Last.fm genre annotations"
date:   2016-08-1 00:00:00
categories:  papers
---

We have prepared a number of genre datasets in the context of our research presented on the 17th International Society for Music Information Retrieval Conference (ISMIR'16) and the 3rd International Digital Libraries for Musicology workshop (DL4M'16). These datasets include genre annotations inferred from Last.fm folksonomy tags found for many recordings in AcousticBrainz. 

## Annotation process
Last.fm tags are freeform, but they tend to include commonly recognized genres. We used the Last.fm API to get tag names and counts for recordings in the AcousticBrainz database. We then filtered these tags to recognize the ones corresponding to genres and organized them according to their specificity and weights by basic string-matching to various genre taxonomies.

### beets genre tree
For our [ISMIR'16 paper](http://mtg.upf.edu/node/3498), we used a [genre tree](https://github.com/beetbox/beets/blob/0c7823b4/beetsplug/lastgenre/genres-tree.yaml) from beets, a popular music tagger software. We matched tags directly to genres or sub-genres in the tree and then mapped them to their top-level genre. Weights were combined for multiple tags mapped to the same top-level genre. Unmatched tags were discarded. We removed tracks where the weight of the top tag was less than 30, normalized the tags so that the top tag had a weight of 100 and again discarded tags with a weight of less than 30. 
    
After the cleaning process, we gathered genre annotations for 778,964 unique MBIDs, corresponding to 1,743,674 AcousticBrainz recordings (including duplicates). These annotations cover 16 top-level genres: african, asian, avant-garde, blues, caribbean and latin american, classical, country, easy listening, electronic, folk, hip hop, jazz, pop, rhythm & blues, rock, and ska.

### Discogs, AllMusis and Itunes genre trees
For our [DL4M'16 paper](http://mtg.upf.edu/node/3533) we decided to go beyond top-level genre annotations and included annotations by specific sub-genres together with their parent genres. We used three genre trees re-constructed from reference pages for [Discogs](https://www.discogs.com/release/add), [AllMusic](http://www.allmusic.com/genres), and [Itunes](https://affiliate.itunes.apple.com/resources/
documentation/genre-mapping).

For each recording, each tag is mapped to a genre and its parent genres. We preserve the tag weights, and the weight of the genre is the sum of its own weight plus the weights of all of its children.

We inferred genre annotations for 841,571 unique MBIDs using the Discogs tree (covering 491 genres, 15 top-level genres), 810,655 using AllMusic (1186 genres, 16 top-level genres) and 788,426 using Itunes (253 genres, 38 top-level genres). The coverage of all three annotations is very intersected (788,426 MBIDs contain annotations in all three datasets).


## Source code
TODO add links.

## Files
TODO add links.
