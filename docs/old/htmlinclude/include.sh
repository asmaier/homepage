#!/bin/sh

java -jar HTMLincl.jar template.html source/ ../
java -jar HTMLincl.jar templatecomp.html source/computer/ ../
java -jar HTMLincl.jar templatelinux.html source/computer/linux ../
