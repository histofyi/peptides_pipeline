
from rich.progress import Progress
from functions import save_progress, process_allele_and_peptide, check_for_processing, load_datasource_metadata, save_status


def process_mhcmotifatlas(**kwargs):

    datasource = 'mhcmotifatlas'

    datasource_metadata = load_datasource_metadata(datasource)

    if check_for_processing(datasource):

        with open(f"{datasource_metadata['tmp_folder']}/{datasource_metadata['filename']}") as f:
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

                        alleles, peptides = process_allele_and_peptide(allele_slug, peptide, alleles, peptides)


                progress.update(task, advance=1)

                i += 1


        save_progress(alleles, peptides, 'mhcmotifatlas')
                        
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

    

        