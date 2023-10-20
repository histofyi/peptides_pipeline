
from rich.progress import Progress
from functions import save_progress

files_to_concatenate = [f'data/netmhcpan_train/c00{number}_el' for number in range(0,5)]

raw_data = ''

peptides = {}
alleles = {}

for file in files_to_concatenate:
    print (f'Current file: {file}')
    f = open(file, "r")
    this_data = f.read()
    raw_data += this_data
    f.close()

to_process = [line for line in raw_data.splitlines() if len(line) > 0]

hla_lines = [line for line in to_process if 'HLA-' in line]

print (f'Number of HLA lines: {len(hla_lines)}')
with Progress() as progress:
        
        i = 0
        task = progress.add_task("[white]Processing...", total=len(hla_lines))

        for line in hla_lines:
            components = line.split(' ')
            peptide = components[0]
            allele = components[2]

            allele_slug = allele.replace('-', '_').replace(':', '_').lower()   
            allele_slug = f"{allele_slug[0:5]}_{allele_slug[5:]}"

            if peptide not in peptides:
                peptides[peptide] = []
            peptides[peptide].append(allele_slug)

            if allele_slug not in alleles:
                alleles[allele_slug] = {
                    'peptide_lengths': {},
                    'count': 0,
                }
            peptide_length = len(peptide)
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

            i += 1

save_progress(alleles, peptides, 'netmhcpan')
                
print (f'Number of unique peptides: {len(peptides)}')
print (f'Number of alleles: {len(alleles)}')