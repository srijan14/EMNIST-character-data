# EMNIST-character-data
This repo contains the code to convert .mat format emnist datafiles to local filesystem for better visualization in a proper formatted order that can be used for training.

### Prerequisites

1. Python 3.7
2. pip 19.0.3

### Installing
```
pip install -r requirements.txt
```

### Running

To convert the eminst data files (.mat format) to local filesystem in a proper train-test split format:

```python create_dataset.py data_path  split_param ```

**data_path** is the path for the .mat file

**split_param** is just a helper string parameter used to signify the split type for folder structure creation. 

### Example

``` python create_dataset.py ./eminst_mat/byclass/emnist-byclass.mat byclass```

Running the above command creates a folder structure, a sample of which is present in the ***sample_output*** folder.

Please read [this](https://www.nist.gov/node/1298471/emnist-dataset) for more details on the dataset and different splits.
