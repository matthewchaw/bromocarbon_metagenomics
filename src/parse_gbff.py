''' for gbff file, read all CDS, get sequence, put data into dataframe.'''

import pandas as pd 
import os 
from Bio import SeqIO

def getFeatures(file):
    
    parsed_features = dict()
    records = 0
    with open(file) as file:
        for record in SeqIO.parse(file, "genbank"):
            records += 1
            # sequence = record.seq
            for feature in record.features:
                if feature.type == "CDS":
                    parsed_features[str(feature.location)] = feature.extract(record.seq)
                else:
                    continue
        # r_c_sequence = sequence.reverse_complement()
        return parsed_features

def main():
    gbff_path = '../gbff/data'
    for f in os.listdir(gbff_path):
        print(f)
        data = {}
        features = getFeatures(os.path.join(gbff_path, f) )
        for feature in features: 
            print(feature)


if __name__ == '__main__':
    main()