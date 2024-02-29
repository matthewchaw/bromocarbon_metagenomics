#!/bin/bash

# Input directory containing SRA files
input_dir="/net/nunn/vol1/chawm/rotation/metagenomes/data/bowman_2023_PRJNA942251/sra"

# Output directory to save FASTA files
output_dir="/net/nunn/vol1/chawm/rotation/metagenomes/data/bowman_2023_PRJNA942251/fasta"

# Path to the giant FASTA file
giant_fasta_file="/net/nunn/vol1/chawm/rotation/metagenomes/data/bowman_2023_PRJNA942251/fasta/all.fasta"

# Count the total number of SRA files
total=$(ls -1 $input_dir/*.sra | wc -l)
count=0

# Create an empty giant FASTA file
> $giant_fasta_file

# Iterate through all SRA files in the input directory
for file in $input_dir/*.sra
do
    # Increment count
    ((count++))

    # Get the filename without extension
    filename=$(basename -- "$file")
    filename_noext="${filename%.*}"

    # Convert the SRA file to FASTQ format
    fastq-dump --fasta --split-files --outdir $output_dir $file

    # Rename the output FASTQ files to FASTA format
    mv $output_dir/${filename_noext}_1.fasta $output_dir/${filename_noext}.fasta

    # Concatenate the current FASTA file to the giant FASTA file
    cat $output_dir/${filename_noext}.fasta >> $giant_fasta_file

    # Calculate progress percentage
    progress=$((count * 100 / total))

    # Output progress bar
    echo -ne "Progress: ["
    for ((i = 0; i < progress / 2; i++)); do
        echo -ne "="
    done
    for ((i = progress / 2; i < 50; i++)); do
        echo -ne " "
    done
    echo -ne "] $progress%\r"
done

echo ""
echo "Conversion and concatenation completed. Giant FASTA file saved as $giant_fasta_file"

