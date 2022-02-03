#!/usr/bin/env bash
# -*- coding: utf-8 -*-
""" select_scos.py

 Select single copy orthologues (SCOs) that are shared between the Pspph candidates but not with other Pseudomonas. 
 This is to reduce the number of orthologues to compute downstream since SCOs shared with all Pseudomonas were not helpful 
 in determining Pspph phylogeny. 
 We have OrthoFinder SCO results for two datasets:

 - large_Pph (lots of Pph, not many other Pseuds)
 - small_Pph (not so many Pph, lots of other Pseuds)

 We want to identify (and later exclude) SCOs from large_Pph that we already saw in small_Pph
 This is because we suspect they do not provide much phylogenetic resolution.

 The way we approach this is to generate some data for each group of SCO sequences:
 - a set of hashes that correspond to the sequences in the SCO group
 So we have a dictionary, keyed by filename/filepath (unique by large_Pph/small_Pph and SCO identifier), containing such a set.
 If we loop over each such filename/SCO ID in the large_Pph group of SCOs, and compare each set of hashes with each set of hashes in the small_Pph group of SCOs,
 then we will know if we've seen that SCO before because there will be an intersection between the sets.

 The general approach is:

 - create a dictionary for small_Pph
 - loop over all SCO FASTA files in small_Pph
 - for each SCO FASTA file, make a new dictionary entry {SCO_ID: set of hashes}
 - loop over all SCO FASTA files in large_Pph
 - create a set of hashes for that file
 - check this set of hashes against each set in the dictionary for small_Pph, stopping if we find an intersection
 - if no intersection was found, indicate this in some way/write out/copy the sequence file 


"""

import os 
import hashlib
import shutil

from pathlib import Path
from Bio import SeqIO

## To do that we need to assign each sequence (corresponding to a unique sco) a unique hash code 
# Defining a function to do  this
def fasta_to_hash_set(fpath):
    """Returns set of unique sequence hashes for a FASTA file"""
    with fpath.open() as ifh:
        seqset = {hashlib.sha256(str(seqrecord.seq).encode("utf-8")).hexdigest() for seqrecord in SeqIO.parse(ifh, "fasta")}
        
    return seqset

# PSYDIR contains the scos that are shared between all reference pseudomonas 
# Each file is a MAFFT alignment 
PSYDIR = Path("./WGS_phylogenetics_Pseudomonas/orthofinder/Results_Nov26/Single_Copy_Orthologue_Sequences")

# PPHDIR contains the scos that are shared between all the Pseudomonas savastanoi pv phaseolicola candidates
PPHDIR = Path("./WGS_phylogenetics_Phaseolicola/orthofinder/Results_Jan25/Single_Copy_Orthologue_Sequences")

# OUTDIR is the location to which selected scos that are unique to PPHDIR (not shared with PSYDIR) will be written
OUTDIR = Path("./WGS_phylogenetics_Phaseolicola/selected_scos")


# Generate dictionary of small_Pph hash sets
small_dict = {}
for fpath in PSYDIR.iterdir():
    small_dict[fpath.stem] = fasta_to_hash_set(fpath)

# Compare each file in large_Pph to all of the small_Pph hash sets
not_seen_before = []

for fpath in PPHDIR.iterdir():
    stem, hashes = fpath.stem, fasta_to_hash_set(fpath)
    seen = False
    for small_hashes in small_dict.values():
        if hashes.intersection(small_hashes):
            seen = True
    if not seen:
        not_seen_before.append(stem)
	
        
print(f"{len(not_seen_before)} SCOs were not seen before")


# make a list of path to the files that passed the test "not seen before"
test_list = not_seen_before
prefix = "./WGS_phylogenetics_Phaseolicola/orthofinder/Results_Jan25/Single_Copy_Orthologue_Sequences/"
prefix_list = [prefix + sub for sub in test_list]
suffix = ".fa"
full_list = [ sub + suffix for sub in prefix_list]
#print(full_list)  # check path list visually 

# copy selection of scos that are uniquely shared between Pph candidates to output folder:
print(f"Writing Pph-unique SCOs files to {OUTDIR}")
os.makedirs(OUTDIR, exist_ok=True)  # Create output directory, if needed
for f in full_list:
    shutil.copy(f, OUTDIR)

print("Done") 

