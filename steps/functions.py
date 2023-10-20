from typing import Dict

import json
import os
import requests
import datetime


def save_progress(alleles:Dict, peptides:Dict, dataset:str):
    with open(f"outputs/{dataset}/alleles.json", "w") as f:
        f.write(json.dumps(alleles, indent=4))
    with open(f"outputs/{dataset}/peptides.json", "w") as f:
        f.write(json.dumps(peptides, indent=4))
    pass


def process_datasource(datasource_key:str):
    datasource_metadata = load_datasource_metadata(datasource_key)

    output, success, errors = download_datasource(datasource_metadata)

    if success:
        if output['changed']:
            print ('Changed')
            print (datasource_metadata['compression'])
            print(output['message'])
        else:
            print ('Unchanged')
            print(output['message'])
    else:
        print(errors)

    return output, success, errors


def load_datasource_metadata(datasource_key:str):
    with open("datasources.json", "r") as f:
        datasources = json.load(f)
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


def decompress(filename:str, output:str, decompression_type:str):
    pass