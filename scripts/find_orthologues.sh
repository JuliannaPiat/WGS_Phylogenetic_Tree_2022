#!/usr/bin/env bash
#
# find_orthologues.sh
#
# Find orthologues using orthofinder

# Change soft limit on simultaneously open files
ulimit -n 15476  

# Run orthofinder
orthofinder -f genomes/proteins -o orthofinder/
