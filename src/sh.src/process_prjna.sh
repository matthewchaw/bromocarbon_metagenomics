#!/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <parent_directory> <bioproject_accession>"
    exit 1
fi

# Assign arguments to variables
parent_dir=$1
bioproject=$2

# Step 1: Prefetch and extract SRA files
mkdir -p $parent_dir/sra
prefetch $bioproject
fastq-dump --split-files --outdir $parent_dir/sra $bioproject

# Step 2: Convert SRA files to FASTA format and concatenate into combined.fasta
mkdir -p $parent_dir/fasta
total=$(ls $parent_dir/sra/*.sra | wc -l)
current=0
for file in $parent_dir/sra/*.sra; do
    fastq-dump --fasta --split-files --outdir $parent_dir/fasta ${file}
    cat $parent_dir/fasta/*${file##*/}.fasta | pv -l -s $(cat $parent_dir/fasta/*${file##*/}.fasta | wc -l) -p -t -e -N "${file##*/}" >> $parent_dir/combined.fasta
    current=$((current+1))
    echo "$current/$total completed"
done

# Step 4: Make a BLAST database from the combined FASTA file
mkdir -p $parent_dir/db
makeblastdb -in $parent_dir/combined.fasta -dbtype nucl -out $parent_dir/db/mydb

echo "Process completed."

