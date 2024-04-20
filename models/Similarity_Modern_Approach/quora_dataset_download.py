from datasets import load_dataset, Dataset

# Load the dataset
raw_datasets = load_dataset("quora")
print("Raw datasets train: ", raw_datasets['train'].features)
raw_datasets["train"].to_json("data/quora_datasets.json")