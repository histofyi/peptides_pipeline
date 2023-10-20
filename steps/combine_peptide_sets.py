
import json

with open('outputs/iedb/alleles.json') as f:
    iedb_alleles = json.load(f)

with open('outputs/netmhcpan/alleles.json') as f:
    netmhcpan_alleles = json.load(f)

with open('outputs/immunopeptidomics_paper/alleles.json') as f:
    immunopeptidomics_alleles = json.load(f)

with open('outputs/mhcmotifatlas/alleles.json') as f:
    mhcmotifatlas_alleles = json.load(f)


alleles = {}
skipped = []

datalabels = ['iedb','netmhcpan','immunopeptidomics','mhcmotifatlas']
i = 0
for dataset in [iedb_alleles, netmhcpan_alleles, immunopeptidomics_alleles, mhcmotifatlas_alleles]:
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
                            alleles[allele]['peptide_lengths'][peptide_length]['peptides'][peptide]['origin'].append(origin)
                            alleles[allele]['peptide_lengths'][peptide_length]['peptides'][peptide]['count'] += 1   
                            alleles[allele]['peptide_lengths'][peptide_length]['count'] += 1
                            alleles[allele]['count'] += 1
                            alleles[allele]['origin'][origin] += 1
        if not proceed:
            skipped.append(f"{datalabels[i]}_{allele}")
    i += 1
    print ('')

print (f'Number of alleles: {len(alleles)}')

print (f"skipped {len(skipped)} alleles:")

print (skipped)

print ('saving...')
with open('outputs/combined/alleles.json', 'w') as outfile:
    json.dump(alleles, outfile, sort_keys=True, indent=4)


for allele in alleles:
    print (allele)
    print (alleles[allele]['origin'])
    print (alleles[allele]['count'])