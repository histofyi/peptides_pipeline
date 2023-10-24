
import json

with open('output/iedb/alleles.json') as f:
    iedb_alleles = json.load(f)

with open('output/netmhcpan/alleles.json') as f:
    netmhcpan_alleles = json.load(f)

with open('output/immunopeptidomics_paper/alleles.json') as f:
    immunopeptidomics_alleles = json.load(f)

with open('output/mhcmotifatlas/alleles.json') as f:
    mhcmotifatlas_alleles = json.load(f)

other_set = mhcmotifatlas_alleles
other_set_label = 'mhcmotifatlas'

first_set = iedb_alleles
first_set_label = 'iedb'


for allele in other_set:
    if allele.count('_') == 3:
        if allele in first_set:
            print (allele)
            if '9' in first_set[allele]['peptide_lengths']:
                first_set_peptides = set(first_set[allele]['peptide_lengths']['9']['peptides'])
            else:
                first_set_peptides = set()
            if '9' in other_set[allele]['peptide_lengths']:
                other_set_peptides = set(other_set[allele]['peptide_lengths']['9']['peptides'])
            else:
                other_set_peptides = set()

            print (f"{len(first_set_peptides.intersection(other_set_peptides))} out of {len(other_set_peptides)} peptides of length 9 in {other_set_label} are in {first_set_label}")

        else:
            print (f'Allele {allele} not found in {first_set_label}')
            if '9' in other_set[allele]['peptide_lengths']:
                print (f"{other_set[allele]['peptide_lengths']['9']['count']} peptides of length 9 in {other_set_label}")
            

        print ('')
