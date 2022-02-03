#!/usr/bin/env bash
#
# build_tree.sh
#
# Build maximum parsimony tree using raxml-ng, with
# bootstrap support

raxml-ng --check \
  --msa selected_concatenated_cds/concatenated.fasta \
  --model selected_concatenated_cds/concatenated.part \
  --prefix tree2/01_check

raxml-ng --parse \
  --msa selected_concatenated_cds/concatenated.fasta \
  --model selected_concatenated_cds/concatenated.part \
  --prefix tree2/02_parse

raxml-ng \
  --msa selected_concatenated_cds/concatenated.fasta \
  --model selected_concatenated_cds/concatenated.part \
  --threads 8 \
  --seed 38745 \
  --prefix tree2/03_infer

raxml-ng --bootstrap \
  --msa selected_concatenated_cds/concatenated.fasta \
  --model selected_concatenated_cds/concatenated.part \
  --threads 8 \
  --seed 38745 \
  --bs-trees 100 \
  --prefix tree2/04_bootstrap

raxml-ng --bsconverge \
  --bs-trees tree2/04_bootstrap.raxml.bootstraps \
  --prefix tree2/05_convergence \
  --seed 1084351 \
  --threads 8 \
  --bs-cutoff 0.01

raxml-ng --rfdist \
  --tree tree2/03_infer.raxml.mlTrees \
  --prefix tree2/06_rfdist

raxml-ng --support \
  --tree tree2/03_infer.raxml.bestTree \
  --bs-trees tree2/04_bootstrap.raxml.bootstraps \
  --prefix tree2/07_support \
  --threads 8
