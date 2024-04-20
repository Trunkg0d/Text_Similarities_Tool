from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np
from nltk.tokenize import sent_tokenize

# device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
model.load_state_dict(torch.load("quora_BERT_finetuning.pth", map_location=torch.device("cpu")))
model.to("cpu")

paragraph1 = """The sunset over the horizon painted the sky in a mesmerizing array of colors. 
                 The golden hues blended seamlessly with the soft purples and pinks, creating a breathtaking panorama. 
                 As the sun dipped lower, it cast long shadows across the landscape, adding depth to the scene. 
                 The tranquil waters of the lake reflected the vibrant colors, doubling the visual splendor. 
                 The serenity of the moment enveloped the onlookers, and a gentle breeze rustled the leaves on the nearby trees. 
                 This tranquil evening marked the perfect end to a long day."""

paragraph2 = """The sun descended below the horizon, adorning the sky with a captivating blend of colors. 
                 Soft purples and pinks intermingled with radiant golden hues, forming a stunning visual display. 
                 As the sun's position lowered, it stretched shadows across the land, infusing the scene with depth. 
                 The lake's placid waters mirrored the vivid hues, intensifying the beauty. 
                 Observers were enveloped in a profound sense of peace, while a gentle breeze gently stirred the leaves on the nearby trees. 
                 This calm evening marked a flawless conclusion to a day well spent."""

sentences1 = sent_tokenize(paragraph1)
sentences2 = sent_tokenize(paragraph2)

sentences = [[s1, s2] for s1 in sentences1 for s2 in sentences2]

tokens = tokenizer(sentences,
    truncation=True, padding=True, return_tensors='pt')

tokens.to("cpu")

logits = model(**tokens).logits
logits = logits.cpu().detach().numpy()
preds = np.argmax(logits, axis=-1)
print(preds)

print("Sentences have the high similarity:")
print()
for ind, pred in enumerate(preds):
    if pred == 1:
        print(sentences[ind])
