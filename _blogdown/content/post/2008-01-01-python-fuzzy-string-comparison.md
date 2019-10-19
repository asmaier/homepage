---
title: Python fuzzy string comparison
author: admin
date: '2008-01-01'
slug: python-fuzzy-string-comparison
categories: []
tags:
  - old_wiki
  - programming
  - python
  - computer
subtitle: ''
summary: ''
authors: []
lastmod: '2019-10-19T22:53:53+02:00'
featured: no
image:
  caption: ''
  focal_point: ''
  preview_only: no
projects: []
---
## Fuzzy string comparison



    >>> import difflib
    >>> s=difflib.SequenceMatcher(None, "abcd","bcde")
    # Return a measure of the sequences’ similarity as a float in the range [0, 1].
    # This is 1.0 if the sequences are identical, and 0.0 if they have nothing in common.
    >>> print s.ratio()
    0.75


### Bibliography
0. <http://stackoverflow.com/questions/682367/good-python-modules-for-fuzzy-string-comparison>  
0. <http://docs.python.org/library/difflib.html>  
