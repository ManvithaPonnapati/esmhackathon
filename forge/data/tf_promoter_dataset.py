import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd

# Custom Dataset class
class TranscriptionFactorDataset(Dataset):
    def __init__(self, csv_file):
        # Load the CSV file into a pandas DataFrame
        self.data = pd.read_csv(csv_file)

    def __len__(self):
        # Return the total number of samples
        return len(self.data)

    def __getitem__(self, idx):
        # Get the transcription factor sequence, DNA sequence, and label
        transcription_factor_seq = self.data.iloc[idx, 0]
        dna_seq = self.data.iloc[idx, 1]
        label = torch.tensor(self.data.iloc[idx, 2], dtype=torch.float32)

        return transcription_factor_seq, dna_seq, label

# Usage example
if __name__ == "__main__":
    csv_file = 'your_data.csv'  # Path to your CSV file

    # Create the dataset and dataloader
    dataset = TranscriptionFactorDataset(csv_file)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Iterate through the dataloader
    for transcription_factor_seq, dna_seq, label in dataloader:
        print(f"Transcription Factor Seq: {transcription_factor_seq}")
        print(f"DNA Seq: {dna_seq}")
        print(f"Label: {label}")
