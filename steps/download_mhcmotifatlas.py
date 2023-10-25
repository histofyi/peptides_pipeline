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
            functions.save_status(datasource_key, 'changed')        
        else:
            functions.save_status(datasource_key, 'unchanged')
        print(output['message'])
    else:
        # if it has failed, output the errors
        functions.save_status(datasource_key, 'errors')
        print(errors)
        
    return {
        'output': output,
        'success': success,
        'errors': errors
    }

if __name__ == "__main__":
    download_mhcmotifatlas()