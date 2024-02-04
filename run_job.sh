#!/bin/bash -l
#
#SBATCH --time=72:00:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --mem=100000
#SBATCH --job-name="ETL_EDGAR_10k_filings"
#SBATCH --output=ETL_EDGAR_10k_filings.out
#SBATCH --mail-user=chitralp@buffalo.edu
#SBATCH --mail-type=end
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute
#SBATCH --cluster=ub-hpc
# Navigate to the directory where you want to run the Python script
cd /projects/academic/haimonti/ETL_10k_filings/word_count/ETL-SEC-EDGAR-10-k-Filings

# Activate your Python virtual environment
source venv/bin/activate

# Run your Python script and use 'tee' for streaming the output
python3 scrape_entire_text_mda.py | tee ETL_SEC_EDGAR_10k_filings_stream.out
