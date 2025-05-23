from rich.progress import Progress
from functions import save_progress, load_datasource_metadata, process_allele_and_peptide, check_for_processing, save_status
from helpers.text import slugify

import os
import csv

def process_iedb(**kwargs):

    datasource = 'iedb'

    datasource_metadata = load_datasource_metadata(datasource)

    if check_for_processing(datasource):

        datasource_metadata = load_datasource_metadata(datasource)

        folder = datasource_metadata['tmp_folder'] + '/data'

        iedb_files = [f"{folder}/{filename}" for filename in os.listdir(folder) if filename.startswith('mhc_ligand_full_')]

        alleles = {}
        peptides = {}

        class_ii_alleles = {}
        class_ii_peptides = {}

        non_class_i_alleles = []
        i = 1

        # a set of hla class I loci to check against
        hla_class_i = ['hla_a','hla_b','hla_c','hla_e','hla_f','hla_g']

        incomplete_hla_class_ii = ['hla_dq', 'hla_dp', 'hla_drb', 'hla_drb1', 'hla_drb3', 'hla_drb4', 'hla_drb5', 'hla_dr', 'hla_dr1', 'hla_dr2', 'hla_dr3', 'hla_dr4', 'hla_dr5']

        for iedb_file in iedb_files:

            data = [row for row in csv.reader(open(iedb_file, "r"), delimiter=",")]

            
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
                    
                    else:
                        if 'hla' in allele_slug:
                            if len(allele_slug) > 7: 
                                if allele_slug not in incomplete_hla_class_ii:
                                    if 'hla_drb' in allele_slug:
                                        allele_slug = allele_slug.replace('hla_drb', 'hla_dra_01_01_drb')
                                        if 'dp' not in allele_slug and 'dq' not in allele_slug and 'mutant' not in allele_slug:
                                            if allele_slug not in non_class_i_alleles:
                                                non_class_i_alleles.append(allele_slug)
                                                print (f"Class II allele found: {allele_slug}")
                                            class_ii_alleles, class_ii_peptides = process_allele_and_peptide(allele_slug, peptide, class_ii_alleles, class_ii_peptides)
                        
                    progress.update(task, advance=1)

            save_progress(alleles, peptides, datasource)
            save_progress(class_ii_alleles, class_ii_peptides, datasource, mhc_class='class_ii')
            i += 1

        print (f'Number of unique peptides: {len(peptides)}')
        print (f'Number of alleles: {len(alleles)}')
        print (f'Non-class I alleles {len(non_class_i_alleles)}')
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