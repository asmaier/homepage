---
title: 'The author seems to suggest ...'
author: admin
date: 2015-10-16
output: pdf_document
categories: []
tags:
- facebook
- german
subtitle: ''
summary: ''
authors: []
lastmod: 2015-10-16T11:17:49+02:00
featured: no
image:
  caption: ''
  focal_point: ''
  preview_only: no
projects: []
slug: []
---
The author seems to suggest that one should use Apache Spark for fluid dynamic simulations. Although this is technically possible I guess the performance will be orders of magnitude slower than using MPI (and this of course is unacceptable if you want to do HIGH performance computing). The reason is that Apache Spark is nothing else than MapReduce on Steroids. And MapReduce is a programming model for problems which don't need a lot of communication (actually in the map step, there is no communication possible between the worker nodes). But fluid dynamic simulations are the opposite of that; you need to communicate with your neighbor cells. Otherwise your fluid will disintegrate into separate blocks, which don't interact with each other (in opposition to what we see in nature).

MPI is old and it misses features like fail-safety (which you don't need on multimillion dollar super computers, because they have fail-safety build into there hardware). But it is still the best tool for a lot of problems, like LaTex is still the best framework for creating books and publications in science (And LaTex is even older than MPI!).﻿
> [![](http://www.dursi.ca)](http://www.dursi.ca/hpc-is-dying-and-mpi-is-killing-it)
> dursi.ca
> ## [Jonathan Dursi](http://www.dursi.ca/hpc-is-dying-and-mpi-is-killing-it)
>
>R&D computing at scale

