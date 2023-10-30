from typing import Dict
import json
from functions import load_datasources_metadata, load_statuses, save_status


def combine_peptide_sets(**kwargs) -> Dict:

    processable = False

    statuses = load_statuses()
    status_list = [statuses[status]['status'] for status in statuses]

    if 'processed' in status_list:
        processable = True

    datasets = {}

    if processable:
        datasources = load_datasources_metadata()

        peptide_allele_combinations = 0

        for datasource in datasources:
            with open(f"output/{datasources[datasource]['processed_folder']}/alleles.json") as f:
                datasets[datasource] = json.load(f)

        alleles = {}
        skipped = []

        datalabels = [datasource for datasource in datasources.keys()]
        i = 0
        for datasource in datasets:
            dataset = datasets[datasource]
            print (f"Processing {datalabels[i]}...")
            for allele in dataset:
                proceed = False
                origin = datalabels[i]
                if not 'mutant' in allele:
                    if not 'class' in allele:
                        if not len(allele) < 10:
                            proceed = True
                            print (f"Processing {allele}...")
                            if allele not in alleles:
                                alleles[allele] = {
                                    'peptide_lengths': {},
                                    'count': 0,
                                    'origin': {}
                                }
                            if origin not in alleles[allele]['origin']:
                                alleles[allele]['origin'][origin] = 0
                            for peptide_length in dataset[allele]['peptide_lengths']:
                                if peptide_length not in alleles[allele]['peptide_lengths']:
                                    alleles[allele]['peptide_lengths'][peptide_length] = {
                                        'peptides': {},
                                        'count': 0
                                    }
                                for peptide in dataset[allele]['peptide_lengths'][peptide_length]['peptides']:
                                    if peptide not in alleles[allele]['peptide_lengths'][peptide_length]['peptides']:
                                        alleles[allele]['peptide_lengths'][peptide_length]['peptides'][peptide] = {
                                            'origin': [],
                                            'count': 0
                                        }
                                        peptide_allele_combinations += 1
                                    alleles[allele]['peptide_lengths'][peptide_length]['peptides'][peptide]['origin'].append(origin)
                                    alleles[allele]['peptide_lengths'][peptide_length]['peptides'][peptide]['count'] += 1   
                                    alleles[allele]['peptide_lengths'][peptide_length]['count'] += 1
                                    alleles[allele]['count'] += 1
                                    alleles[allele]['origin'][origin] += 1
                if not proceed:
                    skipped.append(f"{datalabels[i]}_{allele}")
            i += 1
            save_status(datasource, 'combined')
            print ('')

        print (f'Number of alleles: {len(alleles)}')
        print (f"Number of peptide-allele combinations: {peptide_allele_combinations}")

        print ('saving...')
        with open('output/processed_data/combined/alleles.json', 'w') as outfile:
            json.dump(alleles, outfile, sort_keys=True, indent=4)

        for datasource in datasets:
            save_status(datasource, 'combined')
        
        return {
            'allele_count': len(alleles),
            'peptide_allele_count': peptide_allele_combinations,
            'datasources': datalabels,
            'datasource_count': len(datalabels),
            'status': 'processed'
        }

    else:
        print ('No datasources to process, all up to date.')
        return {
            'status': 'unchanged'
        }
