import json


with open('outputs/netmhcpan/alleles.json') as json_file:
    alleles = json.load(json_file)


labels = []
values = []

for allele in alleles:
    labels.append(allele)
    print (allele)
    if '9' in alleles[allele]['peptide_lengths']:
        values.append(alleles[allele]['peptide_lengths']['9']['count'])
        print (alleles[allele]['peptide_lengths']['9']['count'])
    else:
        values.append(0)
        print (0)

print (len(labels))
print (len(values))