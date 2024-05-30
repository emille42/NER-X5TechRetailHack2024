import torch
import json
from transformers import AutoModelForTokenClassification, AutoTokenizer
from transformers import pipeline
import zipfile


# unzip downloaded model
with zipfile.ZipFile("solution3.zip","r") as zip_ref:
    zip_ref.extractall("./results/")

# Load the fine-tuned model
model = AutoModelForTokenClassification.from_pretrained("./results/solution")
tokenizer = AutoTokenizer.from_pretrained("./results/solution")

# Determine the device
device = torch.device("mps" if torch.has_mps else "cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()
pipe = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy='average')

with open("data/test.json", "r") as file:
    data = json.load(file)


# Make predictions on the test set and format the results
predictions_output = []
for item in data:
    text = item["text"]

    ner_results = pipe(text)

    for entity in ner_results:
         entity.pop("score")
         entity["word"] = text[entity["start"]:entity["end"]]

    predictions_output.append({"text" : text, "entities" : ner_results})

output_file = "data/submission.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(predictions_output, f, ensure_ascii=False, indent=4)

    print(f"Predictions saved to {output_file}")