import functions


def download_mhcmotifatlas(**kwargs):
    """
    This function downloads the MHC Motif Atlas from the Gfeller Lab.
    
    """
    datasource_key = 'mhcmotifatlas'

    print ('Downloading data from MHC Motif Atlas...')

    output, success, errors = functions.process_datasource(datasource_key)

    if success:
        if output['changed']:                
            print(output['message'])
        else:
            print(output['message'])
    else:
        print(errors)

    return {
        'output': output,
        'success': success,
        'errors': errors
    }

if __name__ == "__main__":
    download_mhcmotifatlas()