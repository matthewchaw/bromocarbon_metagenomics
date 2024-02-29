import pandas as pd 
import os 

def main():
    file = '../output/snow_ice_ocean_genes_proteins.csv'
    df = pd.read_csv(file) 
    df.fillna('None', inplace=True)
    with open('../output/query_fasta.fasta', 'w') as f:
        genes = df['gene'].to_list() 
        products = df['product'].to_list()
        ids = df['id'].to_list() 
        seqs = df['sequence'].to_list()
        organisms = df['organism'].to_list()
        feature_id = df['feature_id']
        for i in range(len(genes)):
            f.write(f'>{organisms[i]}|{ids[i]}|{feature_id[i]}|{genes[i]}|{products[i]}\n'.replace(' ', '_'))
            f.write(f'{seqs[i]}\n')

if __name__ == '__main__':
    main()