#!/usr/bin/env bash
#
# align_scos.sh
#
# Align single-copy orthologue sequences using MAFFT

# Create output directory
mkdir -p selected_sco_proteins_aligned

# Align each set of SCOs
for fname in selected_scos/*.fa
do
    mafft --thread 12 ${fname} > selected_sco_proteins_aligned/`basename ${fname%%.fa}`_aligned.fasta
done
