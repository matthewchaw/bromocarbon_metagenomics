''' for gbff file, read all CDS, get sequence, put data into dataframe.'''

import pandas as pd 
import os 
from Bio import SeqIO
import pdb

def getFeatures(file):
    
    parsed_features = dict()
    records = 0
    with open(file) as file:
        parsed_features = {
            'location':[],
            'sequence':[],
            'id':[],
            'description':[],
            'translation':[],
            'gene':[],
            'product':[],
            'note':[]
        }
        for record in SeqIO.parse(file, "genbank"):
            records += 1
            organism = None
            # sequence = record.seq
            for feature in record.features:

                if feature.type == 'source': 
                    # pdb.set_trace()
                    organism = str(feature.qualifiers['organism'][0])

                if feature.type == "CDS":
                    parsed_features['location'].append(str(feature.location))
                    parsed_features['sequence'].append(str(feature.extract(record.seq)))
                    parsed_features['id'].append(str(record.id))
                    parsed_features['description'].append(str(record.description))

                    for qual in ['translation', 'gene', 'product', 'note']:
                        try:
                            parsed_features[qual].append(str(feature.qualifiers[qual][0]))
                        except KeyError: 
                            parsed_features[qual].append(None)
                else:
                    continue
        parsed_features['organism'] = [organism]*len(parsed_features['location'])
        # r_c_sequence = sequence.reverse_complement()
        return parsed_features

def main():
    gbff_path = '../gbff/data'
    dfs = []
    for f in os.listdir(gbff_path):
        data = {}
        features = getFeatures(os.path.join(gbff_path, f) )
        dfs.append(pd.DataFrame.from_dict(features))
    df = pd.concat(dfs)
    df.sort_values('organism', inplace=True)
    df.reset_index(inplace=True)
    df['feature_id'] = df.index
    df.to_csv('../output/snow_ice_ocean_genes_proteins.csv', index=False)
if __name__ == '__main__':
    main()