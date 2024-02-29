#!/bin/bash
# Check if the number of arguments is correct
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

module load modules modules-init modules-gs
module load sratoolkit/3.0.0
module load ncbi-blast/2.7.1
query_fasta="/net/nunn/vol1/chawm/rotation/metagenomes/src/query_fasta.fasta"
db_dir=$1

blastn -db "$db_dir/db" -query "$query_fasta" -out "$db_dir/blastn_output.txt" -outfmt 6

