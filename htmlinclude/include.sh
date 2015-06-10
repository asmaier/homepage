#!/bin/sh

java -jar HTMLincl.jar template.html source/ destination/
java -jar HTMLincl.jar templatecomp.html source/computer/ destination/
java -jar HTMLincl.jar templatelinux.html source/computer/linux destination/
