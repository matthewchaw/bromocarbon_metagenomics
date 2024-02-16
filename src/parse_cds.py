''' Read cds, determine if gene in list of genes is present.
then, read genome sequence using blast to determine if gene is actually present 
but not documented? 
'''
import os
import pdb
from Bio import SeqIO, Seq
import numpy as np 
import pandas as pd
import timeit
import re

def getPOI(file):
    ''' retrieve proteins of interest from csv. 
    '''
    df = pd.read_csv(file)

    return df

# def parseElement(feature, element, keywords, grant_name, proteins_df):
#     ''' 
#     check whether any keywords in proteins df are  in 
#     the cds qualifier. 
#     Ex. feature.qualifier['element'] = 'VANADIUM BROMOPEROXIDASE'
#     keyword  in row of  proteins_df: ['VANADIUM, BROMOPEROXIDASE, VBPO']'
#     return another  df

#     element is a key in the feature.qualifiers dictionary. 
#     '''



def getFeatures2(file, proteins_df):
    genes = proteins_df['short_name'].dropna().str.upper().to_list()
    # print(genes)
    # kwords = 
    kw = proteins_df['keywords'].dropna().str.upper().to_list()
    # grant = proteins_df['grant_application_name'].dropna().str.upper().to_list()
    keywords = list()
    for k in kw+genes:
        if k.split(' '):
            keywords += k.strip().split(',')
        else:
            keywords.append(k.strip())
    keywords = [k.strip() for k in keywords if k]
    
    # keywords = keywords+genes+grant
    # print(keywords)

    for record in SeqIO.parse(file, "genbank"):
        print('>',record.description)
        for feature in record.features: 
            if feature.type == 'CDS':
                try:
                    # print(record.description, feature.qualifiers["gene"][0].upper().strip())
                    if feature.qualifiers["gene"][0].upper().strip() in genes:
                        print(f'gene. {feature.qualifiers["gene"]} encodes protein of interest')
                except KeyError:
                    quals = ['note', 'notes', 'product']
                    for qual in quals:
                        try:
                            cds_attr = feature.qualifiers[qual][0].upper().split(' ')
                            counter = 0
                            for kw in keywords:
                                # print(kw)
                                if kw in cds_attr:
                                    counter += 1
                                    print( kw)
                            if counter > 2 and counter/len(cds_attr) >= 0.66:
                                print(counter, cds_attr)
                        except KeyError: 
                            pass 
def getFeatures(file, proteins_df):
    genes = proteins_df['short_name'].str.upper().to_list()
    # kwords = 
    keywords = proteins_df['keywords'].str.upper().to_list()
    grant = proteins_df['grant_application_name'].str.upper().to_list()
    keywords = keywords+genes+grant

    # grant_name = proteins_df['grant_application_name'].str.upper().to_list()
    dfs = list()
    for record in SeqIO.parse(file, "genbank"):
        print('>',record.description)
        for feature in record.features: 
            if feature.type == 'CDS':
                try:
                    if feature.qualifiers["gene"][0].upper() in genes:
                        df = proteins_df.loc[proteins_df['short_name'].str.upper() == feature.qualifiers["gene"][0].upper()]
                        # print(dir(feature.extract(record.seq)))
                        data = {
                            'gene': [str(feature.qualifiers['gene'][0])],
                            'id': [str(record.id)],
                            'description':[str(record.description)],
                            'sequence':[str(feature.extract(record.seq))],
                            'location':[str(feature.location)],
                            'translation':[str(feature.qualifiers['translation'][0])]
                        }
                        for d in data.keys():
                            df = pd.DataFrame(data)
                        dfs.append(df)
                except KeyError:
                    # print('key error') 
                    pass
    if len(dfs) == 0: 
        return None
    else:
        dfs = pd.concat(dfs)
        return dfs
            
def main(): 
    path = '../gbff/data'
    genomes = os.listdir(path)
    records = dict() 
    proteins_df = pd.read_csv('../proteins/antarctic_proteins_keywords.csv')
    dfs = list()
    for i, genome in enumerate(genomes): 
        df = getFeatures(os.path.join(path, genome), proteins_df)
        dfs.append(df)
    df = pd.concat(dfs)
    df.to_csv('../proteins/genes_nucs_aa.csv', index=False)

        # pdb.set_trace()
        #f.features[n].qualifiers.gene
        #f.features[n].qualifiers.product
        #f.features[10].extract(f.seq)

if __name__ == '__main__':
    main() 