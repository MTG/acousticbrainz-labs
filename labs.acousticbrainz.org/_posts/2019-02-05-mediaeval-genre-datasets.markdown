---
layout: post
title:  "MediaEval AcousticBrainz Genre Task datasets"
date:   2019-02-5 00:00:00
categories:  datasets
---

Over the past two years, we’ve been working on a genre recognition task based on the vast amounts of music data we gathered in the AcousticBrainz database. We presented this task at [MediaEval](http://www.multimediaeval.org/) [2017](https://multimediaeval.github.io/2017-AcousticBrainz-Genre-Task/) and [2018](https://multimediaeval.github.io/2018-AcousticBrainz-Genre-Task/), a benchmarking initiative that organizes an annual cycle of scientific evaluation tasks in the area of multimedia access and retrieval.

The task is about music genre recognition: we want to build systems that are able to predict genre and subgenre of unknown music recordings (tracks) given automatically computed music audio features of those recordings. What makes it different from other genre classification tasks is that our goal is to explore how the same music pieces can be annotated differently by different communities following different genre taxonomies, and how this should be addressed by content-based genre recognition systems.

Having run this task for two consecutive years, we received a number of solutions to this complex problem. We now provide the development and validation datasets used in this challenge for researchers willing to continue on the task. To make the access and referencing to the data easier we share it at Zenodo:
- https://zenodo.org/record/2553414
- https://zenodo.org/record/2554044

We provide music features from AcousticBrainz and four datasets containing genre and subgenre annotations of recordings extracted from four different online metadata sources:

- **AllMusic** and **Discogs** are based on editorial metadata databases maintained by music experts and enthusiasts. These sources contain explicit genre/subgenre annotations of music releases (albums) following a predefined genre namespace and taxonomy. We propagated release-level annotations to recordings (tracks) in AcousticBrainz to build the datasets.

- **Lastfm** and **Tagtraum** are based on collaborative music tagging platforms with large amounts of genre labels provided by their users for music recordings (tracks). We have automatically inferred a genre/subgenre taxonomy and annotations from these labels.

For details on format and contents, please refer to the [data webpage](https://multimediaeval.github.io/2018-AcousticBrainz-Genre-Task/data/).
