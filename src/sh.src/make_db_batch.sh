#!/bin/bash

# Check if the number of arguments is correct
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Input directory containing the files
input_dir="$1"

# Get the sister directory
sister_dir="$(dirname "$input_dir")/db"

# Create the sister directory if it does not exist
mkdir -p "$sister_dir"

# Loop through each file in the input directory
for file in "$input_dir"/*; do
    # Check if the file is a regular file
    if [ -f "$file" ]; then
        # Get the filename without the directory path
        filename=$(basename "$file")
        # Run makeblastdb for the file
        makeblastdb -in "$file" -dbtype nucl -out "$sister_dir/${filename}_db"
    fi
done

echo "BLAST databases created in $sister_dir."

