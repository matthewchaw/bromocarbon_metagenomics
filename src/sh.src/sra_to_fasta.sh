#!/bin/bash

# Input directory containing SRA files
input_dir="/net/nunn/vol1/chawm/rotation/metagenomes/data/bowman_2023/sra"

# Output directory to save FASTA files
output_dir="/net/nunn/vol1/chawm/rotation/metagenomes/data/bowman_2023/fasta"

# Iterate through all SRA files in the input directory
for file in $input_dir/*.sra
do
    # Get the filename without extension
    filename=$(basename -- "$file")
    filename_noext="${filename%.*}"

    # Convert the SRA file to FASTQ format
    fastq-dump --fasta 0 --split-files --outdir $output_dir $file

    # Rename the output FASTQ files to FASTA format
    mv $output_dir/${filename_noext}_1.fasta $output_dir/${filename_noext}.fasta
done

echo "Conversion completed."

