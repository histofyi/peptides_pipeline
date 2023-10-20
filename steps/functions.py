import json


def save_progress(alleles, peptides, dataset):
    with open(f"outputs/{dataset}/alleles.json", "w") as f:
        f.write(json.dumps(alleles, indent=4))
    with open(f"outputs/{dataset}/peptides.json", "w") as f:
        f.write(json.dumps(peptides, indent=4))
    pass