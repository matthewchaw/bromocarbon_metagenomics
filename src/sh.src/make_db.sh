#!/bin/bash
# Check if the number of arguments is correct
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Input directory containing FASTA files
input_dir="$1"

# Check if input directory exists
if [ ! -d "$input_dir" ]; then
    echo "Directory not found: $input_dir"
    exit 1
fi

# Temporary file for concatenated data
temp_file="$input_dir/temp.fasta"
echo "Concatenating files"
# Concatenate all FASTA files in the input directory
cat "$input_dir"/*.fasta > "$temp_file"
echo "Files concatenated. Generating DB."

# Create the output directory for the database if it does not exist
output_dir="$input_dir/../db"
mkdir -p "$output_dir"

# Create a BLAST database from the concatenated data
makeblastdb -in "$temp_file" -dbtype nucl -out "$output_dir/db"

# Check if makeblastdb was successful
if [ $? -ne 0 ]; then
    echo "Error creating BLAST database. Exiting."
    exit 1
fi

# Remove the temporary file
rm "$temp_file"

echo "BLAST database created in $output_dir."

