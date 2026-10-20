# CHEM501_Workshop5
## Data Analysis

In this workshop we'll scipy to analyse the data you gather using your Arduino and explore the capabilities of matplotlib a bit more.

## Setting up your Computer
You'll need to install the following modules to do this workshop:

1. pyserial
2. pandas
3. numpy
4. matplotlib
5. scipy

There are two options to install these:

### Create a conda environment
Run the following in your Terminal / Anaconda Prompt:

```bash
conda create -n chem501_w5
conda activate chem501_w5
conda install python pyserial pandas numpy matplotlib scipy
```

### Install via pip
Clone the git repo to an appropriate directory and run the following:

```bash
cd chem501_w5
pip install requirements.txt
```