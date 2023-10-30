import csv_to_sqlite 
from functions import load_datasources_metadata, load_statuses, save_status
import os

def convert_csv_to_sqlite(**kwargs):
    """
    This function converts the combined dataset CSV file to a SQLite database.
    """

    processable = False

    statuses = load_statuses()
    status_list = [statuses[status]['status'] for status in statuses]



    if 'combined_to_csv' in status_list:
        processable = True

    if processable:

        sql_lite_filename = "output/processed_data/combined/peptides.sqlite"
        csv_filename = "output/processed_data/combined/peptides.csv"

        if os.path.exists(sql_lite_filename):
            print ('Removing existing SQLite file...')
            os.remove(sql_lite_filename)

        options = csv_to_sqlite.CsvOptions()
        csv_to_sqlite.write_csv([csv_filename], sql_lite_filename, options)

        datalabels = [datasource for datasource in load_datasources_metadata()]


        for datasource in datalabels:
            print (f"Saving status for {datasource}...")
            save_status(datasource, 'combined_to_sqlite')

        print ('Data written to SQLite.')

        return {
            'status': 'combined_to_sqlite'
        }
    else:
        print ("Data does not need to be processed, either because it is unchanged or previous steps have not yet been run. Please check the status.json file.")
        return {
            'status': 'unchanged'
        }


if __name__ == "__main__":
    convert_csv_to_sqlite()