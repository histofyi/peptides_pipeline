from create_folder_structure import create_folder_structure

from download_netmhcpan import download_netmhcpan
from download_mhcmotifatlas import download_mhcmotifatlas
from download_iedb import download_iedb
from download_cedar import download_cedar

from process_mhcmotifatlas import process_mhcmotifatlas
from process_netmhcpan import process_netmhcpan
from process_iedb import process_iedb
from process_cedar import process_cedar

from combine_peptide_sets import combine_peptide_sets
from convert_combined_to_csv import convert_combined_to_csv
from convert_csv_to_sqlite import convert_csv_to_sqlite

steps = {
    '1':{
        'function':create_folder_structure,
        'title_template':'the folder structure used by the pipeline.',
        'title_verb':['Creating','Creates'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '2':{
        'function':download_mhcmotifatlas,
        'title_template':'the MHC Motif Atlas dataset.',
        'title_verb':['Downloading','Downloads'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '3':{
        'function':download_netmhcpan,
        'title_template':'the NetMHCPan training dataset.',
        'title_verb':['Downloading','Downloads'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '4':{
        'function':download_iedb,
        'title_template':'the IEDB epitope dataset.',
        'title_verb':['Downloading','Downloads'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '5':{
        'function':download_cedar,
        'title_template':'the CEDAR epitope dataset.',
        'title_verb':['Downloading','Downloads'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '6':{
        'function':process_mhcmotifatlas,
        'title_template':'the MHC Motif Atlas dataset.',
        'title_verb':['Processing','Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '7':{
        'function':process_netmhcpan,
        'title_template':'the NetMHCPan training dataset.',
        'title_verb':['Processing','Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '8':{
        'function':process_iedb,
        'title_template':'the IEDB epitope dataset.',
        'title_verb':['Processing','Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '9':{
        'function':process_cedar,
        'title_template':'the CEDAR cancer epitope dataset.',
        'title_verb':['Processing','Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '10':{
        'function':combine_peptide_sets,
        'title_template':'the peptide/allele datasets from the different datasources.',
        'title_verb':['Combining','Combines'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '11':{
        'function':convert_combined_to_csv,
        'title_template':'the combined dataset to a CSV file.',
        'title_verb':['Converting','converts'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '12':{
        'function':convert_csv_to_sqlite,
        'title_template':'the combined dataset to a sqlite file.',
        'title_verb':['Converting','converts'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    }
}