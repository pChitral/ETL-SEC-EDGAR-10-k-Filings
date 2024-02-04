#!/bin/bash -l
#
#SBATCH --time=72:00:00
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=16
#SBATCH --mem=100000
#SBATCH --job-name="ETL_EDGAR_10k_filings"
#SBATCH --output=ETL_EDGAR_10k_filings.out
#SBATCH --mail-user=chitralp@buffalo.edu
#SBATCH --mail-type=end
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute


cd /projects/academic/haimonti/ETL_10k_filings/word_count/ETL-SEC-EDGAR-10-k-Filings

source venv/bin/activate


python3 scrape_entire_text_mda.py | tee ETL_SEC_EDGAR_10k_filings_stream.out
