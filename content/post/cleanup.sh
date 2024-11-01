#!/bin/bash

mkdir -p temp
for file in *.md; do
  if [ -d "${file%.*}" ]; then
    mv "$file" temp
  fi
done