from create_folder_structure import create_folder_structure

from download_netmhcpan import download_netmhcpan
from download_mhcmotifatlas import download_mhcmotifatlas
from download_iedb import download_iedb
from download_cedar import download_cedar

from process_mhcmotifatlas import process_mhcmotifatlas
from process_netmhcpan import process_netmhcpan

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
    }
}