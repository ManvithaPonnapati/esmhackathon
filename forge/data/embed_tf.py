from huggingface_hub import login
import esm
from esm.models.esm3 import ESM3
from esm.sdk.api import ESM3InferenceClient, ESMProtein, SamplingConfig
import pandas as pd
import torch

# Login to Hugging Face using your token
login(token='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')

# Download the model weights and instantiate the model on your machine
model: ESM3InferenceClient = ESM3.from_pretrained("esm3-open").to("cuda")  # Use "cpu" if not using CUDA

# Function to embed protein sequences using ESM3 and save the embeddings
def embed_protein_sequences(tsv_file, output_file):
    # Load the TSV file containing protein sequences
    df = pd.read_csv(tsv_file, sep='\t')

    # Step 1: Sort the DataFrame by the 'Sequence' column
    df = df.sort_values(by='Sequence')

    # Initialize an empty list to hold embeddings
    all_embeddings = []

    # Loop through each sequence in the sorted DataFrame
    for sequence in df['Sequence']:
        # Step 2: Prepare the protein sequence for the ESM3 model
        protein = ESMProtein(sequence=sequence)

        # Step 3: Encode the sequence to get the embeddings
        protein_tensor = model.encode(protein)

        # Step 4: Run the forward pass to get per-residue embeddings
        output = model.forward_and_sample(
            protein_tensor, SamplingConfig(return_per_residue_embeddings=True)
        )

        # Step 5: Get the per-residue embedding and mean-pool over the sequence
        sequence_embedding = output.per_residue_embedding.mean(dim=0)
        print(sequence_embedding.shape, sequence_embedding)
        # Append the embedding to the list
        all_embeddings.append(sequence_embedding)

    # Step 6: Concatenate all embeddings into a single tensor
    all_embeddings_tensor = torch.stack(all_embeddings, dim=0)  # [num_sequences, hidden_size]

    # Step 7: Save the concatenated tensor to a file
    torch.save(all_embeddings_tensor, output_file)
    print(f"Embeddings saved to {output_file}")

if __name__ == "__main__":
    # Path to the input TSV file containing protein sequences
    protein_tsv_file = "/home/ubuntu/bigtune/evolve24/transcription_factors.tsv"

    # Path to save the concatenated tensor
    output_tensor_file = "protein_embeddings.pt"

    # Call the function to embed and save
    embed_protein_sequences(protein_tsv_file, output_tensor_file)
