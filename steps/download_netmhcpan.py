import functions
import os


def download_netmhcpan(**kwargs):
    """
    This function downloads the NetMHCpan data dump from the Nielsen Lab.
    """
    datasource_key = 'netmhcpan'

    print ('Downloading data from NetMHCpan...')

    output, success, errors = functions.process_datasource(datasource_key)

    datasource_metadata = functions.load_datasource_metadata(datasource_key)

    if success:
        if output['changed']:
            # set variables
            folder = datasource_metadata['tmp_folder']
            filename = datasource_metadata['filename']
            extraction_folder = datasource_metadata['extraction_folder']
            unzipped = f"{datasource_metadata['filename'].replace('.gz','')}"
            
            print ('Gunzipping and extracting')
            # gunzip the downloaded file
            os.system(f"gunzip -k {folder}/{filename}")
            # extract the files from the tar file
            os.system(f"tar -xf {folder}/{unzipped} -C {folder}")

            print ('Cleaning up')
            # remove the tar file
            os.system(f"rm {folder}/{unzipped}")
            # remove the data folder if it exists (this will be stale data)
            os.system(f"rm -r {folder}/data")
            
            print ('Moving directory contents to data folder')
            # move the extracted files to the data folder
            os.system(f"mv {folder}/{extraction_folder} {folder}/data")
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
    download_netmhcpan()