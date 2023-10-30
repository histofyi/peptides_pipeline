from typing import Dict

from pipeline import Pipeline

from steps import steps

def run_pipeline(**kwargs) -> Dict:
    pipeline = Pipeline()

    pipeline.load_steps(steps)

    pipeline.run_step('1') # create folder structure
    #pipeline.run_step('2') # download mhcmotifatlas
    #pipeline.run_step('3') # download netmhcpan
    #pipeline.run_step('4') # download iedb
    #pipeline.run_step('5') # download cedar
    pipeline.run_step('6') # process mhcmotifatlas
    pipeline.run_step('7') # process netmhcpan
    pipeline.run_step('8') # process iedb
    pipeline.run_step('9') # process cedar
    pipeline.run_step('10') # combine peptide sets
    pipeline.run_step('11') # convert combined set to csv
    pipeline.run_step('12') # convert csv to sqlite

    action_logs = pipeline.finalise()

    return action_logs

def main():

    output = run_pipeline()

if __name__ == '__main__':
    main()