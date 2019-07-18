# Cleansing Youtube Trending Data in Kaggle

This repo contains scripts for data cleasning of a dataset in [Kaggle](https://www.kaggle.com/datasnaek/youtube). Scripts are written in Python 3.

## Pre-requisites

- Clone this repo
- Makes 2 folders under this repo: `raw` and `cleansed`, save all data in `raw` from Kaggle
- Install Python 3
- Install required dependencies by `pip install -r requirements.txt`

Optional: to run the Jupyter Notebook in `notebook`, please also install `jupyter`

## Details

The dataset includes data from Youtube that are in trending category in GB and US during the period 2017-09-13 to 2017-10-22. There are around 200 videos in each day per country. 

To clean the data and output them to `cleansed`, use

`python3 clean_data.py`

A detailed discussion on how to clean this dataset is available in `notebook`.

Two json manifest files are also provided if one is interested to visualize the data in AWS QuickSight, a BI tool developed by AWS. Please be reminded to change `<BUCKET_NAME>` to your own S3 bucket name.

## Remarks

There is actually an updated version of this dataset in [Kaggle](https://www.kaggle.com/datasnaek/youtube-new). But I did not check if this repo can be used to clean the new dataset.
