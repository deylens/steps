#!/bin/bash

while IFS= read -r line; do
  [[ -z "$line" || "$line" == \#* ]] && continue
  eval "export $line"
done < .env