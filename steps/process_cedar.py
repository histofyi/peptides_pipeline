from rich.progress import Progress
from functions import save_progress, load_datasource_metadata, process_allele_and_peptide, check_for_processing, save_status
from helpers.text import slugify

import os
import csv

def process_cedar(**kwargs):

    datasource = 'cedar'

    datasource_metadata = load_datasource_metadata(datasource)

    if check_for_processing(datasource):

        datasource_metadata = load_datasource_metadata(datasource)

        folder = datasource_metadata['tmp_folder'] + '/data'

        iedb_files = [f"{folder}/{filename}" for filename in os.listdir(folder) if filename.startswith('mhc_ligand_full_')]

        alleles = {}
        peptides = {}

        i = 1
        for iedb_file in iedb_files:

            data = [row for row in csv.reader(open(iedb_file, "r"), delimiter=",")]

            # a set of hla class I loci to check against
            hla_class_i = ['hla_a','hla_b','hla_c','hla_e','hla_f','hla_g']

            with Progress() as progress:

                task = progress.add_task(f"[white]Processing file {i} of {len(iedb_files)}...", total=len(data))

                for row in data:
                    # information from IEDB is in columns of the CSV, peptide is row 11, allele is row 107
                    peptide = row[11]
                    if ' ' in peptide:
                        peptide = peptide.split(' ')[0]
                    allele_slug = slugify(row[107])

                    # TODO need to do some further checks on the allele slug to make sure it's valid
                    # e.g. hla_b44 is valid for the class I locus, but contains too little information to be useful
                    # in addition there are some mutated, non-natural hla alleles with epitopes in IEDB
                    if allele_slug[0:5] in hla_class_i:
                        
                        alleles, peptides = process_allele_and_peptide(allele_slug, peptide, alleles, peptides)
                        
                    progress.update(task, advance=1)

            save_progress(alleles, peptides, datasource)
            i += 1

        print (f'Number of unique peptides: {len(peptides)}')
        print (f'Number of alleles: {len(alleles)}')
        save_status(datasource, 'processed')
        return {
            'allele_count': len(alleles),
            'peptide_count': len(peptides),
            'status': 'processed'
        }
    else:
        print (f"Data is up to date. No processing needed for {datasource}")
        return {
            'status': 'unchanged'
        }