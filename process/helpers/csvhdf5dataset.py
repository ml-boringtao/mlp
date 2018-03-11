import h5py
import os
import numpy as np

class CSVDatasetWriter:
    def __init__(self, outputPath, data, labels):
        if os.path.exists(outputPath):
            os.remove(outputPath)

        self.db = h5py.File(outputPath, "w")
        self.data = self.db.create_dataset("data", data = data)
        self.labels = self.db.create_dataset("labels", data = labels)
        print('Rewrite the dataset.')
        self.db.close()

    def close(self):
        self.db.close()

class CSVDatasetReader:
    def __init__(self, inputPath):
        if not os.path.exists(inputPath):
            raise ValueError("The dataset can not be found.")

        self.db = h5py.File(inputPath, "r")
    
    def load(self):
        data = self.db['data']
        labels = self.db['labels']
        
        return (np.array(data), np.array(labels))
        self.db.close()
    
    def close(self):
        self.db.close()