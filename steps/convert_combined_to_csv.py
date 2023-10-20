import json
import csv
import pandas as pd

print ("Starting up...")

print ("Loading combined dataset...")
with open('outputs/combined/alleles.json') as f:
    alleles = json.load(f)


fields = ['allele','allele_group','locus','peptide','peptide_length','iedb','netmhcpan','immunopeptidomics','mhcmotifatlas']

for i in range(1,21):
    fields.append(f"P{i}")

dataframe = []
datalabels = ['iedb','netmhcpan','immunopeptidomics','mhcmotifatlas']


print ("Processing combined dataset...")

peptide_lengths = []

for allele in alleles:
    print (allele)
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
                
                datarow = [allele,allele_group,locus,peptide,int(peptide_length),origins['iedb'],origins['netmhcpan'],origins['immunopeptidomics'],origins['mhcmotifatlas']]
                
                for i in range(1,21):
                    if i <= int(peptide_length):
                        datarow.append(peptide[i-1])
                    else:
                        datarow.append('')
                dataframe.append(datarow)
    print ('')

print (f"Number of rows: {len(dataframe)}")

print ("Writing combined dataset to CSV...")
df = pd.DataFrame(dataframe)
df.to_csv('outputs/combined/peptides.csv', index=False, header=fields)


