from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn as nn
import numpy as np
from nltk.tokenize import sent_tokenize
from torch.nn.utils.rnn import pad_sequence, pad_packed_sequence, pack_padded_sequence


class EmbeddingLSTMNet(nn.Module):
    def __init__(self, num_vocab, embedding_dim, hidden_cells,
                 num_layers, embedding_rquires_grad, dropout):
        super(EmbeddingLSTMNet, self).__init__()
        self.dropout = nn.Dropout(dropout)
        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_cells,
            num_layers=num_layers,
            batch_first=True
        )
        self.fc1 = nn.Linear(hidden_cells, hidden_cells)
        self.fc2 = nn.Linear(hidden_cells, hidden_cells)
        self.relu = nn.ReLU()
        # initialize embeddings
        # self.embedding = nn.Embedding.from_pretrained(pretrained_weights)
        self.embedding = nn.Embedding(num_embeddings=num_vocab + 1, embedding_dim=embedding_dim)
        self.embedding.weight.requires_grad = embedding_rquires_grad

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def forward(self, question, lengths):
        """
        Params:
        -------
        question : (batch dim, sequence)
                   i.e. [ [i1, i2, i3],
                          [j1, j2, j4, j5] ]
        lenghts : list
                  list all the lengths of each question

        Return:
        -------
        result : torch.tensor
                 output tesnor of of forward pass
        """
        # Reverse the sequence lengths indices in decreasing order (pytorch requirement for pad and pack)
        sorted_indices = np.flipud(np.argsort(lengths))
        lengths = np.flipud(np.sort(lengths))
        lengths = lengths.copy()

        # Reorder questions in the decreasing order of their lengths
        ordered_questions = [torch.LongTensor(question[i]).to(self.device) for i in sorted_indices]
        # Pad sequences with 0s to the max length sequence in the batch
        ordered_questions = pad_sequence(ordered_questions, batch_first=True)
        # Retrieve Embeddings
        embeddings = self.embedding(ordered_questions).to(self.device)

        # Model forward
        embeddings = self.dropout(embeddings)
        # Pack the padded sequences and pass it through LSTM
        packed = pack_padded_sequence(embeddings, lengths, batch_first=True)
        out, (hn, cn) = self.lstm(packed)
        # Unpack the padded sequence and pass it through the linear layers
        unpacked, unpacked_len = pad_packed_sequence(out, batch_first=True, total_length=int(lengths[0]))
        out = self.fc1(unpacked)
        out = self.relu(out)
        out = self.fc2(out)

        # Reorder the output to the original order in which the questions were passed
        result = torch.FloatTensor(out.size())
        for i, encoded_matrix in enumerate(out):
            result[sorted_indices[i]] = encoded_matrix
        return result


class SiameseNetwork(nn.Module):
    def __init__(self, embedding_lstm_net):
        super(SiameseNetwork, self).__init__()
        """
        Siamese LSTM Network 

        Params:
        -------
        embedding_lstm_net : nn.Module embedded LSTM Network 
        """
        self.embedding = embedding_lstm_net

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def forward(self, q1, q2, q1_lengths, q2_lengths):
        """ Forward pass
        Params:
        -------
        q1 : pad sequence tensor question 1
        q2 : pad sequence tensor question 2
        q1_lengths : torch.tensor original lengths of each question 1
        q2_lengths : torch.tensor original lengths of each question 1
        Returns:
        --------
        similarity_score : torch.tensor
        """
        output_q1 = self.embedding(q1, q1_lengths)
        output_q2 = self.embedding(q2, q2_lengths)
        similarity_score = torch.zeros(output_q1.size()[0]).to(self.device)
        # Calculate Similarity Score between both questions in a single pair
        for index in range(output_q1.size()[0]):
            # Sequence lenghts are being used to index and retrieve the activations before the zero padding since they were not part of original question
            q1 = output_q1[index, q1_lengths[index] - 1, :]
            q2 = output_q2[index, q2_lengths[index] - 1, :]
            similarity_score[index] = self.manhattan_distance(q1, q2)

        return similarity_score

    def manhattan_distance(self, q1, q2):
        """ Computes the Mannhatten distance between the two question tokens """
        return torch.exp(-torch.sum(torch.abs(q1 - q2), dim=0)).to(self.device)

    def cosine_similarity(self, q1, q2):
        cos = nn.CosineSimilarity(dim=0, eps=1e-6)
        return cos(q1, q1)


num_vocab = 86206
embedding_dim = 300
hidden_cells = 100
num_layers = 3
embedding_rquires_grad = False
dropout = 0.0

# embedding net
embedding_net = EmbeddingLSTMNet(
    num_vocab = num_vocab,
    embedding_dim = embedding_dim,
    hidden_cells = hidden_cells,
    num_layers = num_layers,
    embedding_rquires_grad = embedding_rquires_grad,
    dropout = dropout)

# siamese models
model = SiameseNetwork(embedding_net).to("cpu")


model.load_state_dict(torch.load("Model_6_val_acc_82.6406321490843", map_location=torch.device("cpu")))
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
