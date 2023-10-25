
from rich.progress import Progress
from functions import save_progress, load_datasource_metadata, process_allele_and_peptide, check_for_processing, load_datasource_metadata, save_status
import os


def process_netmhcpan(**kwargs):

    datasource = 'netmhcpan'

    datasource_metadata = load_datasource_metadata(datasource)

    if check_for_processing(datasource):

        folder = datasource_metadata['tmp_folder'] + '/data'

        files_to_concatenate = [f"{folder}/{filename}" for filename in os.listdir(folder) if '_el' in filename]

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

        print (f'Number of data rows to process: {len(hla_lines)}')

        with Progress() as progress:
                
                i = 0
                task = progress.add_task("[white]Processing...", total=len(hla_lines))

                for line in hla_lines:
                    components = line.split(' ')
                    peptide = components[0]
                    allele = components[2]

                    allele_slug = allele.replace('-', '_').replace(':', '_').lower()   
                    allele_slug = f"{allele_slug[0:5]}_{allele_slug[5:]}"

                    alleles, peptides = process_allele_and_peptide(allele_slug, peptide, alleles, peptides)

                    progress.update(task, advance=1)

                    i += 1

        save_progress(alleles, peptides, 'netmhcpan')
                        
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