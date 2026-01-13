# API for Project Sonar
Python package to work with **Project Sonar** datasets and obtain **reordered/cleaned pandas DataFrames** for:
- **FDNS – A**
- **FDNS – TXT** (standard: **DKIM**, **DMARC**, **SPF**, **STS**)
- **TCP**

This project is also meant as a starting point for a **functional programming** approach in Python.

> **Note:** This repository does **NOT** include Project Sonar databases.  
> Datasets can be downloaded from Rapid7 Open Data: https://opendata.rapid7.com/

## What is Project Sonar (in this context)
Project Sonar provides large-scale Internet scan datasets (e.g., DNS / forward DNS and other protocols).  
This repository focuses on utilities to **load, transform, and analyze** those datasets locally.

## Requirements
- Python 3.x
- Common data tooling (typical): `pandas`, `numpy`, `matplotlib` / `seaborn`, `jupyter`
  - Install what you need based on your usage (scripts vs notebook).
> If the repo contains a `requirements.txt`, prefer installing from it.
Create and activate a virtual environment (recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate
```
## Install dependencies
If you have a requirements file:
```bash
pip install -r requirements.txt
```
Otherwise install the common stack:
```bash
pip install pandas numpy matplotlib jupyter
```
## Download Project Sonar datasets
- Download the datasets you want (FDNS-A / FDNS-TXT / TCP) from: https://opendata.rapid7.com/
- Unzip/decompress them locally.

## Usage (Typical Workflow)
- Download the Sonar dataset of interest (e.g., FDNS-A or FDNS-TXT).
- Point your code/notebook to the dataset files stored locally.
- Use the modules in this repo (especially under protocols/) to:
  - parse/ingest data
  - reorder fields
  - build a pandas DataFrame for analysis
- Optionally:
  - use charts.py for plots
  - use evaluation_security.ipynb for an example analysis flow

## License
This project is released under the MIT License.
