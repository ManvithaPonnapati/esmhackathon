import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import numpy as np

# Load transcription factor sequences, pass them through ESM3, and save embeddings
def process_esm3(csv_file, output_file):
    # Load ESM3 model and tokenizer
    esm3_model_name = "EvolutionaryScale/esm3-sm-open-v1"
    esm3_tokenizer = AutoTokenizer.from_pretrained(esm3_model_name)
    esm3_model = AutoModel.from_pretrained(esm3_model_name)

    # Load CSV file
    df = pd.read_csv(csv_file)

    embeddings = []
    for sequence in df['transcription_factor_seq']:
        inputs = esm3_tokenizer(sequence, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = esm3_model(**inputs)
        sequence_embedding = outputs.last_hidden_state.mean(dim=1)  # Mean pooling to get a fixed-size embedding
        sequence_embedding = torch.nn.functional.pad(sequence_embedding, (0, 2300-sequence_embedding.shape[1]))  # Pad to 2300
        embeddings.append(sequence_embedding.squeeze().numpy())

    # Save embeddings as a numpy array
    np.save(output_file, np.array(embeddings))
    print(f"ESM3 embeddings saved to {output_file}")

# Load DNA sequences, pass them through DNABERT, and save embeddings
def process_dnabert(csv_file, output_file):
    # Load DNABERT model and tokenizer
    dnabert_model_name = "zhihan1996/DNABERT-2-117M"
    dnabert_tokenizer = AutoTokenizer.from_pretrained(dnabert_model_name)
    dnabert_model = AutoModel.from_pretrained(dnabert_model_name)

    # Load CSV file
    df = pd.read_csv(csv_file)

    embeddings = []
    for sequence in df['dna_seq']:
        inputs = dnabert_tokenizer(sequence, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = dnabert_model(**inputs)
        sequence_embedding = outputs.last_hidden_state.mean(dim=1)  # Mean pooling to get a fixed-size embedding
        sequence_embedding = torch.nn.functional.pad(sequence_embedding, (0, 2300-sequence_embedding.shape[1]))  # Pad to 2300
        embeddings.append(sequence_embedding.squeeze().numpy())

    # Save embeddings as a numpy array
    np.save(output_file, np.array(embeddings))
    print(f"DNABERT embeddings saved to {output_file}")

if __name__ == "__main__":
    # Process transcription factor sequences
    transcription_factor_csv = "transcription_factors.csv"  # Input CSV with transcription factor sequences
    esm_output_file = "transcription_factor_embeddings.npy"  # Output file for ESM3 embeddings
    process_esm3(transcription_factor_csv, esm_output_file)

    # Process DNA sequences
    dna_csv = "dna_sequences.csv"  # Input CSV with DNA sequences
    dnabert_output_file = "dna_embeddings.npy"  # Output file for DNABERT embeddings
    process_dnabert(dna_csv, dnabert_output_file)

