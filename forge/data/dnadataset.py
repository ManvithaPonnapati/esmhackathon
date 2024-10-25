import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd

class DNADataset(Dataset):
    def __init__(self, pt_file):
        """
        Args:
            pt_file (str): Path to the .pt file containing DNA embeddings.
            dataframe (pd.DataFrame): DataFrame for looking up 388-length arrays based on keys.
        """
        # Load the .pt file which contains DNA embeddings
        self.embeddings_dict = torch.load(pt_file,weights_only=True)
        
        # Store the DataFrame for the lookup
        self.dataframe = pd.read_csv("/home/ubuntu/trimmed_means-2.csv")

        # Get the list of keys (gene IDs or similar) to be used for lookup
        self.keys = list(self.embeddings_dict.keys())

    def __len__(self):
        # Return the total number of samples
        return len(self.keys)

    def __getitem__(self, idx):
        # Get the key for this index
        key = self.keys[idx]
        print(key)
        
        # Get the pEmbedding of size [870, 1536] from the embeddings dictionary
        pEmbedding = torch.load("/home/ubuntu/NeuroForge/forge/data/protein_embeddings.pt",weights_only=True)  # Ensure 
        print(pEmbedding.shape)
        # Get the nEmbedding of size [1, 256] from the embeddings dictionary
        nEmbedding = self.embeddings_dict[key].view(1, 256)  # Ensure correct shape
        
        # Lookup the 388-length array from the DataFrame using the key
    
        layer_out = torch.tensor(self.dataframe.loc[self.dataframe['feature'] == key].iloc[:, 4:391].astype(float).values.flatten().tolist())
        
        # Return the embeddings and the layer_out array
        return pEmbedding, nEmbedding, layer_out