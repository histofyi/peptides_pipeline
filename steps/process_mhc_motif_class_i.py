
from rich.progress import Progress
from functions import save_progress

with open('data/mhcmotifatlas/data.txt') as f:
    raw_data = f.read()

peptides = {}
alleles = {}


to_process = [line for line in raw_data.splitlines() if len(line) > 0]


with Progress() as progress:
        
    i = 0
    task = progress.add_task("[white]Processing...", total=len(to_process))

    for line in to_process:
        if i > 0:       
            components = line.split('\t')
            peptide = components[1]
            allele = components[0]
            if not 'h2-' in allele.lower():

                allele_slug = f"hla_{allele[0].lower()}_{allele[1:3]}_{allele[3:]}"

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


save_progress(alleles, peptides, 'mhcmotifatlas')
                
print (f'Number of unique peptides: {len(peptides)}')
print (f'Number of alleles: {len(alleles)}')