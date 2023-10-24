import pandas as pd 

from rich.progress import Progress
from functions import save_progress, process_allele_and_peptide


excel_file = "data/immunopeptidomics_paper/41587_2019_322_MOESM3_ESM.xlsx"
  
sheets = ['A0101', 'A0201', 'A0202', 'A0203', 'A0204', 'A0205', 'A0206', 'A0207', 'A0211', 'A0301', 'A1101', 'A1102', 'A2301', 'A2402', 'A2407', 'A2501', 'A2601', 'A2902', 'A3001', 'A3002', 'A3101', 'A3201', 'A3301', 'A3303', 'A3401', 'A3402', 'A3601', 'A6601', 'A6801', 'A6802', 'A7401', 'B0702', 'B0704', 'B0801', 'B1301', 'B1302', 'B1402', 'B1501', 'B1502', 'B1503', 'B1510', 'B1517', 'B1801', 'B2705', 'B3501', 'B3503', 'B3507', 'B3701', 'B3801', 'B3802', 'B4001', 'B4002', 'B4006', 'B4201', 'B4402', 'B4403', 'B4501', 'B4601', 'B4901', 'B5001', 'B5101', 'B5201', 'B5301', 'B5401', 'B5501', 'B5502', 'B5601', 'B5701', 'B5703', 'B5801', 'B5802', 'C0102', 'C0202', 'C0302', 'C0303', 'C0304', 'C0401', 'C0403', 'C0501', 'C0602', 'C0701', 'C0702', 'C0704', 'C0801', 'C0802', 'C1202', 'C1203', 'C1402', 'C1403', 'C1502', 'C1601', 'C1701', 'G0101', 'G0103', 'G0104']

alleles = {}
peptides = {}

for sheet in sheets:
    allele_slug = f"hla_{sheet[0].lower()}_{sheet[1:3]}_{sheet[3:]}"

    print (allele_slug)

    with Progress() as progress:

        alleles[allele_slug] = {
            'peptide_lengths': {},
            'count': 0
        }
        df = pd.DataFrame(pd.read_excel(excel_file, sheet_name=sheet))
        allele_peptides = df['sequence'].tolist()
            
        task = progress.add_task("[white]Processing...", total=len(allele_peptides))

        for peptide in allele_peptides:

            alleles, peptides = process_allele_and_peptide(allele_slug, peptide, alleles, peptides)

            progress.update(task, advance=1)
        
        print (f"{len(allele_peptides)} peptides processed")


save_progress(alleles, peptides, 'immunopeptidomics_paper')
                
print (f'Number of unique peptides: {len(peptides)}')
print (f'Number of alleles: {len(alleles)}')