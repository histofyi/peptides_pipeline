from typing import Dict, Union, List, Tuple

import json
import os
import requests
import datetime


def save_progress(alleles:Dict, peptides:Dict, dataset:str):
    """
    This function saves the progress of the pipeline to a JSON file.

    Args:
        alleles (Dict): A dictionary of alleles.
        peptides (Dict): A dictionary of peptides.
        dataset (str): The name of the dataset.

    Returns:
        None
    """
    with open(f"outputs/{dataset}/alleles.json", "w") as f:
        f.write(json.dumps(alleles, indent=4))
    with open(f"outputs/{dataset}/peptides.json", "w") as f:
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
    This function loads the metadata for a specific datasource e.g. iedb for the IEDB datasource.
    
    Args:
        datasource_key (str): The key of the datasource.
    
    Returns:
        Dict: A dictionary of the datasource metadata.
    """
    # Loads the metadata concerning the datasource, e.g. the URL, filename, etc.
    with open("datasources.json", "r") as f:
        datasources = json.load(f)
    # Returns the metadata for the specific datasource
    return datasources[datasource_key]


def download_datasource(datasource:Dict):
    folder = datasource['folder']
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