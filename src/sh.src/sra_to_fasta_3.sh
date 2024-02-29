#!/bin/bash
module load modules modules-init modules-gs
module load sratoolkit/3.0.0
# Check if the number of arguments is correct
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Path to the directory containing the files
directory=$1

# Check if the 'fasta' directory exists, if not, create it
if [ ! -d "$directory/../fasta" ]; then
    mkdir "$directory/../fasta"
fi

# Get the total number of files in the directory
total_files=$(find "$directory" -maxdepth 1 -type f | wc -l)
current_file=0

# Loop through each file in the directory
for file in $directory/*; do
    # Check if the file is a regular file
    if [ -f "$file" ]; then
        # Increment the current file count
        ((current_file++))
        # Run fastq-dump command on the file
	echo "$directory/../fasta/$(basename $file).fasta"
        fastq-dump --split-files --fasta 150 --outdir $directory/../fasta $file
        # Calculate and show the progress bar
        progress=$(echo "scale=2; $current_file * 50 / $total_files" | bc)
        progress_int=${progress%.*}
        progress_dec=${progress#*.}
        echo -ne "Progress: [$((progress_int * 2))%] ["
        for ((i=0; i<progress_int; i++)); do echo -n "#"; done
        if [ "$progress_dec" -gt 0 ]; then echo -n "#"; fi
        for ((i=progress_int; i<50; i++)); do echo -n " "; done
        echo -ne "]\r"
    fi
done

echo "Conversion completed."

