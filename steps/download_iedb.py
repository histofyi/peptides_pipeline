import functions
import os



def download_iedb():
    """
    This function downloads the MHC peptide epitope data dump from the IEDB.

    """

    datasource_key = 'iedb'

    output, success, errors = functions.process_datasource(datasource_key)

    datasource_metadata = functions.load_datasource_metadata(datasource_key)

    if success:
        if output['changed']:
            # set variables
            folder = datasource_metadata['folder']
            filename = datasource_metadata['filename']

            print ('Unzipping and extracting')
            # remove the data folder if it exists (this will be stale data)
            os.system(f"rm -r {folder}/data")

            # unzip the downloaded file into the data folder
            os.system(f"unzip {folder}/{filename} -d {folder}/data")
            
        # output the message from the download step    
        print(output['message'])
    else:
        # if it has failed, output the errors
        print(errors)


if __name__ == "__main__":
    download_iedb()