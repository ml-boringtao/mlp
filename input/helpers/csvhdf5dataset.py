import h5py
import os
import numpy as np
from sklearn import preprocessing

class CSVDatasetProcessor:
    def __init__(self, dataset, fields):
        self.dataset = dataset
        self.fields = fields
    
    def zero_to_median(self):
        for field in self.fields :
            nonzero_vals = self.dataset.loc[self.dataset[field] != 0, field]
            avg = nonzero_vals.median()
            length = len(self.dataset.loc[ self.dataset[field] == 0, field])   # num of 0-entries
            self.dataset.loc[ self.dataset[field] == 0, field ] = avg
            print('Field: %s; fixed %d entries with value: %.3f' % (field,length,avg))

class CSVDatasetWriter:
    def __init__(self, outputPath, dataset):
        try:
            if os.path.exists(outputPath):
                os.remove(outputPath)
        except: 
            pass

        data = dataset.values
        X = data[:,0:8]
        Y = data[:,8]
        X_scale = preprocessing.scale(X)
        #X_normal = preprocessing.normalize(X)
        self.db = h5py.File(outputPath, "w")
        self.data = self.db.create_dataset("data", data = X_scale)
        self.labels = self.db.create_dataset("labels", data = Y)
        print('Rewrite the data in "' + outputPath + '".')

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
    
    def close(self):
        self.db.close()