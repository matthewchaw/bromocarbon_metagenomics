''' Read cds, determine if gene in list of genes is present.
then, read genome sequence using blast to determine if gene is actually present 
but not documented? 
'''

from Bio import SeqIO, Seq
import numpy as np 
import math
import pdb
import sys
import timeit
np.set_printoptions(suppress=True)


def getFeatures(file):
    
    parsed_features = dict()
    records = 0
    for record in SeqIO.parse(file, "genbank"):
        records += 1
        sequence = record.seq
        for feature in record.features:
            if feature.type == "CDS":
                if '<' in str(feature.location) or '>' in str(feature.location):
                    continue
                else:
                    parsed_features[str(feature.location)] = [feature, feature.extract(record.seq)]
            else:
                continue
    r_c_sequence = sequence.reverse_complement()
    return parsed_features, sequence, r_c_sequence
