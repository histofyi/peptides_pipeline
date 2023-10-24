import functions


def download_mhcmotifatlas():
    """
    This function downloads the MHC Motif Atlas from the Gfeller Lab.
    
    """
    datasource_key = 'mhcmotifatlas'

    output, success, errors = functions.process_datasource(datasource_key)

    if success:
        if output['changed']:                
            print(output['message'])
        else:
            print(output['message'])
    else:
        print(errors)


if __name__ == "__main__":
    download_mhcmotifatlas()