#!/bin/bash -l
set -e  # Exit immediately if a command exits with a non-zero status.

#SBATCH --time=24:00:00              # Specify the maximum runtime (here, 24 hours)
#SBATCH --nodes=1                    # Specify the number of nodes (here, 1)
#SBATCH --ntasks-per-node=16          # Specify the number of tasks per node (here, 16)
#SBATCH --mem=75000                  # Specify the memory requirement in MB (75 GB = 75000 MB)
#SBATCH --job-name="ETL_SEC_EDGAR_10k_filings"   # Specify the job name
#SBATCH --output=ETL_SEC_EDGAR_10k_filings.out   # Specify the output file
#SBATCH --error=ETL_SEC_EDGAR_10k_filings.err    # Specify the error file
#SBATCH --mail-user=chitralp@buffalo.edu         # Specify your email address
#SBATCH --mail-type=end
#SBATCH --partition=general-compute              # Specify the partition (general-compute)
#SBATCH --qos=general-c+                         # Updated QoS setting
#SBATCH --cluster=ub-hpc                         # Specify the cluster name (ub-hpc)

# [Rest of your script]

# Navigate to the directory where you want to run the Python script
cd /user/chitralp/ETL-10-k-Filings

# Activate your Python virtual environment
source venv/bin/activate

# Run your Python script and use 'tee' for streaming the output
python3 scrape_entire_text_mda.py | tee ETL_SEC_EDGAR_10k_filings_stream.out

# Deactivate the virtual environment when done
deactivate
