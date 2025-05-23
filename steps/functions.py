from typing import Dict, Union, List, Tuple

import json
import os
import requests
import datetime

status_filename = 'tmp/status.json'


def check_for_processing(datasource:str) -> bool:
    """
    This function checks if a datasource needs to be processed. 
    It does this by:
        - checking if the output files already exist 
        - checking in the log for the pipeline if the download was successful and has changed

    Args:
        datasource (str): The name of the datasource.

    """
    to_process = []
    if load_status(datasource)['status'] == 'changed':
        return True
    else:
        for filecontents in ['alleles', 'peptides']:
            filename = datasource_filename(filecontents, datasource)
            if os.path.exists(filename):
                to_process.append(False)
            else:
                to_process.append(True)
        to_process_set = list(set(to_process))
        if len(to_process_set) == 1:
            return to_process_set[0]
        else:
            return True


def save_status(datasource:str, status:str):
    """
    This function saves the status of the different datasources to a JSON file.

    Statuses are:
        - changed: the datasource has changed and needs to be processed
        - unchanged: the datasource has not changed and does not need to be processed
        - errors: the datasource has errors and needs to be checked
        - processed: the datasource has been processed

    Args:
        datasource (str): The name of the datasource.
        status (str): The status of the datasource.

    """
    # if the status file is not there, create it
    if not os.path.exists(status_filename):
        os.system(f"touch {status_filename}")
        statuses = {}
    else:
        # if it is there, try to load the current json in the file
        try:
            with open(status_filename, 'r') as f:
                statuses = json.load(f)
        except:
            statuses = {}
    # update the status for the datasource
    statuses[datasource] = {
        'status':status,
        'updated_at': datetime.datetime.now().isoformat()
    }
    # then write the statuses out to the file
    with open(status_filename, 'w') as f:
        f.write(json.dumps(statuses, indent=4))
    pass


def load_statuses() -> Dict:
    statuses = None
    with open(status_filename, 'r') as f:
        statuses = json.load(f)
    return statuses


def load_status(datasource:str) -> Dict:
    """
    This function loads the status of a specific datasource from the JSON file.

    Args:
        datasource (str): The name of the datasource.
    
    Returns:
        Dict: A dictionary of the status of the datasource.
    """
    default_status = {'status':'unknown', 'updated_at':None}
    if os.path.exists(status_filename):
        with open(status_filename, 'r') as f:
            statuses = json.load(f)
        if datasource in statuses:
            return statuses[datasource]
        else:
            return default_status
    else:
        return default_status


def datasource_filename(filecontents:str, datasource:str) -> str:
    return f"output/processed_data/{datasource}/{filecontents}.json"


def save_progress(alleles:Dict, peptides:Dict, datasource:str, mhc_class:str='class_i') -> None:
    """
    This function saves the progress of the pipeline to a JSON file.

    It saves JSON data for peptides and alleles in a consistent format.

    Args:
        alleles (Dict): A dictionary of alleles.
        peptides (Dict): A dictionary of peptides.
        datasource (str): The name of the datasource.
        mhc_class (str): The MHC class of the alleles and peptides.

    Returns:
        None
    """
    if mhc_class == 'class_i':
        alleles_name = 'alleles'
        peptides_name = 'peptides'
    elif mhc_class == 'class_ii':
        alleles_name = 'class_ii_alleles'
        peptides_name = 'class_ii_peptides'

    with open(datasource_filename(alleles_name, datasource), "w") as f:
        f.write(json.dumps(alleles, indent=4))
    with open(datasource_filename(peptides_name, datasource), "w") as f:
        f.write(json.dumps(peptides, indent=4))
    pass


def process_datasource(datasource_key:str) -> Union[Dict, bool, List]:
    """
    This function processes a datasource. e.g. the IEDB datasource.

    Args:
        datasource_key (str): The key of the datasource.

    Returns:
        Union[Dict, bool, List]: A tuple containing the output, success and errors.
    """
    # Loads the metadata concerning the datasource, e.g. the URL, filename, etc.
    datasource_metadata = load_datasource_metadata(datasource_key)

    # Fetches the data for the datasource and saves it to a file if it has changed
    output, success, errors = download_datasource(datasource_metadata)
    
    return output, success, errors


def load_datasource_metadata(datasource_key:str) -> Dict:
    """
    This function loads the metfolder
        datasource_key (str): The key of the datasource.
    
    Returns:
        Dict: A dictionary of the datasource metadata.
    """
    # Loads the metadata concerning the datasource, e.g. the URL, filename, etc.
    datasources = load_datasources_metadata()
    # Returns the metadata for the specific datasource
    return datasources[datasource_key]


def load_datasources_metadata() -> Dict:
    """
    This function loads the metadata for all datasources.

    Returns:
        Dict: A dictionary of the datasource metadata.
    """
    # Loads the metadata concerning the datasource, e.g. the URL, filename, etc.
    with open("input/datasources.json", "r") as f:
        datasources = json.load(f)
    return datasources



def download_datasource(datasource:Dict):
    folder = datasource['tmp_folder']
    filename = datasource['filename']
    filname = f"{folder}/{filename}"

    if not os.path.exists(folder):
        os.makedirs(folder)

    output, success, errors = fetch_url(datasource['url'], filname)
    
    return output, success, errors


def fetch_url(url:str, filename:str):
    download = False
    success = False
    errors = []
    output = None
    old_filename = filename
    message = None
    if os.path.exists(filename):

        r = requests.head(url, headers={'Accept-Encoding': None})

        if 'Content-Length' in r.headers:
            if int(r.headers['Content-Length']) != os.path.getsize(filename):
                download = True
            else:
                success = True
                output = {
                    'filename': filename,
                    'size': os.path.getsize(filename),
                    'downloaded_at': datetime.datetime.fromtimestamp(os.stat(filename).st_mtime).isoformat(),
                    'message': 'File already exists and is up to date',
                    'changed': False,
                }
        else:
            filename = f"{filename}.new"
            errors.append(f"Failed to get Content-Length for {url}")
            download = True
    else:
        download = True

    if download:
        download_command = f"wget {url} -O {filename}"
        os.system(download_command)   

        if os.path.exists(filename):
            if '.new' in filename:
                if os.path.getsize(old_filename) != os.path.getsize(filename):
                    os.remove(old_filename)
                    os.rename(filename, old_filename)
                    filename = old_filename
                    message = 'File replaced'
                    changed = True
                else:
                    os.remove(filename)
                    filename = old_filename
                    message = 'File already exists and is up to date'
                    changed = False
            else:
                message = 'File downloaded'
                changed = True
            success = True
            output = {
                'filename': filename,
                'size': os.path.getsize(filename),
                'downloaded_at': datetime.datetime.now().isoformat(),
                'message': message,
                'changed': changed
            }
        else:
            errors.append(f"Failed to download {url} to {filename}")
    return output, success, errors





def process_allele_and_peptide(allele_slug:str, peptide:str, alleles:Dict, peptides:Dict) -> Union[Dict, Dict]:
    """
    This function processes information on the combination of an allele and peptide into consistent dictionaries

    Args:
        allele_slug (str): The slug of the allele.
        peptide (str): The peptide.
        alleles (Dict): A dictionary of alleles.
        peptides (Dict): A dictionary of peptides.

    Returns:
        Union[Dict, Dict]: A tuple containing the alleles and peptides dictionaries.
    """
    # If the peptide is not in the peptides dictionary, add it
    if peptide not in peptides:
        peptides[peptide] = []
    # If the allele is not in the peptides dictionary, add it
    if allele_slug not in peptides[peptide]:
        peptides[peptide].append(allele_slug)
    
    # Next get the length of the peptide
    peptide_length = len(peptide)

    # If the slugified allele number is not in the alleles dictionary, add it
    if allele_slug not in alleles:
        alleles[allele_slug] = {
            'peptide_lengths': {},
            'count': 0
    }

    # If the peptide length is not in the alleles dictionary, add it
    if peptide_length not in alleles[allele_slug]['peptide_lengths']:
        alleles[allele_slug]['peptide_lengths'][peptide_length] = {
            'peptides': [],
            'count': 0
        }
    # Finally if the peptide is not in the alleles dictionary in the specific peptide length/allele slug combination, add it
    if peptide not in alleles[allele_slug]['peptide_lengths'][peptide_length]['peptides']:
        alleles[allele_slug]['peptide_lengths'][peptide_length]['peptides'].append(peptide)
        # and increment the counts
        alleles[allele_slug]['peptide_lengths'][peptide_length]['count'] += 1
        alleles[allele_slug]['count'] += 1

    # Return the updated dictionaries
    return alleles, peptides