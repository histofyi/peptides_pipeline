from rich.progress import Progress
from functions import save_progress
from helpers.text import slugify

import csv

iedb_files = [f"data/iedb/mhc_ligand_full_0{i}.csv" for i in range(1, 8)]

alleles = {}
peptides = {}

for iedb_file in iedb_files:

    data = [row for row in csv.reader(open(iedb_file, "r"), delimiter=",")]

    hla_class_i = ['hla_a','hla_b','hla_c','hla_e','hla_f','hla_g']


    with Progress() as progress:

        task = progress.add_task("[white]Processing...", total=len(data))

        for row in data:
            peptide = row[11]
            if ' ' in peptide:
                peptide = peptide.split(' ')[0]
            allele_slug = slugify(row[107])

            if allele_slug[0:5] in hla_class_i:
                
                if peptide not in peptides:
                    peptides[peptide] = []
                peptides[peptide].append(allele_slug)
                
                peptide_length = len(peptide)

                if allele_slug not in alleles:
                    alleles[allele_slug] = {
                        'peptide_lengths': {},
                        'count': 0
                }

                if peptide_length not in alleles[allele_slug]['peptide_lengths']:
                    alleles[allele_slug]['peptide_lengths'][peptide_length] = {
                        'peptides': [],
                        'count': 0
                    }
                if peptide not in alleles[allele_slug]['peptide_lengths'][peptide_length]['peptides']:
                    alleles[allele_slug]['peptide_lengths'][peptide_length]['peptides'].append(peptide)
                    alleles[allele_slug]['peptide_lengths'][peptide_length]['count'] += 1
                    alleles[allele_slug]['count'] += 1
                
            progress.update(task, advance=1)

    save_progress(alleles, peptides, 'iedb')

    print (f'Number of unique peptides: {len(peptides)}')
    print (f'Number of alleles: {len(alleles)}')