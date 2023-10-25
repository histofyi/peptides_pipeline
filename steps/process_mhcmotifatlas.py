
from rich.progress import Progress
from functions import save_progress, process_allele_and_peptide


def process_mhcmotifatlas(**kwargs):

    if 'datehash' in kwargs:
        datehash = kwargs['datehash']
    
    print (datehash)

    with open('data/mhcmotifatlas/data.txt') as f:
        raw_data = f.read()

    peptides = {}
    alleles = {}

    to_process = [line for line in raw_data.splitlines() if len(line) > 0]