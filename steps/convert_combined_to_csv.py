import json
import csv
import pandas as pd
from functions import load_datasources_metadata, load_statuses, save_status


def convert_combined_to_csv(**kwargs):
    """
    This function converts the combined dataset to a CSV file.
    """

    processable = False

    statuses = load_statuses()
    status_list = [statuses[status]['status'] for status in statuses]

    if 'combined' in status_list:
        processable = True

    datalabels = [datasource for datasource in load_datasources_metadata()]

    if processable:


        print ("Loading combined dataset...")
        with open('output/processed_data/combined/alleles.json') as f:
            alleles = json.load(f)


        fields = ['allele','allele_group','locus','peptide','peptide_length']

        for datasource in datalabels:
            fields.append(datasource)

        for i in range(1,21):
            fields.append(f"P{i}")

        dataframe = []


        print ("Processing combined dataset...")

        peptide_lengths = []

        for allele in alleles:
            print (f"Processing {allele}")
            for peptide_length in alleles[allele]['peptide_lengths']:
                if peptide_length not in peptide_lengths:
                    peptide_lengths.append(peptide_length)
                
                if int(peptide_length) <= 20:
                    for peptide in alleles[allele]['peptide_lengths'][peptide_length]['peptides']:
                        allele_group = allele[0:8]
                        locus = allele[0:5]
                        origins = {}
                        for datalabel in datalabels:
                            if datalabel in alleles[allele]['peptide_lengths'][peptide_length]['peptides'][peptide]['origin']:
                                origins[datalabel] = True
                            else:
                                origins[datalabel] = False
                        
                        datarow = [allele,allele_group,locus,peptide,int(peptide_length)]

                        for datasource in datalabels:
                            datarow.append(origins[datasource])
                        
                        for i in range(1,21):
                            if i <= int(peptide_length):
                                datarow.append(peptide[i-1])
                            else:
                                datarow.append('')
                        dataframe.append(datarow)

        print (f"Number of rows: {len(dataframe)}")

        print ("Writing combined dataset to CSV...")
        df = pd.DataFrame(dataframe)
        df.to_csv('output/processed_data/combined/peptides.csv', index=False, header=fields)


        for datasource in datalabels:
            print (f"Saving status for {datasource}...")
            save_status(datasource, 'combined_to_csv')

        print ('Data written to CSV.')

        return {
            'status': 'combined_to_csv',
            'rows': len(dataframe)
        }
    else:
        print ("Data does not need to be processed, either because it is unchanged or previous steps have not yet been run. Please check the status.json file.")
        return {
            'status': 'unchanged'
        }