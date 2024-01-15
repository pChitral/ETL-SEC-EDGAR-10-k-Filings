#!/bin/bash -l
#
#SBATCH --time=24:00:00       # Specify the maximum runtime (here, 24 hours)
#SBATCH --nodes=32             # Specify the number of nodes (here, 32)
#SBATCH --ntasks-per-node=32  # Specify the number of tasks per node (here, 32)
#SBATCH --mem=100000           # Specify the memory requirement in MB (100 GB = 100000 MB)
#SBATCH --job-name="ETL_SEC_EDGAR_10k_filings"  # Specify the job name
#SBATCH --output=ETL_SEC_EDGAR_10k_filings.out  # Specify the output file
#SBATCH --mail-user=chitralp@buffalo.edu        # Specify your email address
#SBATCH --mail-type=end
#SBATCH --partition=general-compute             # Specify the partition (general-compute)
#SBATCH --qos=general-compute                   # Specify the quality of service (general-compute)
#SBATCH --cluster=ub-hpc                        # Specify the cluster name (ub-hpc)

# Navigate to the directory where you want to run the Python script
cd /user/chitralp/ETL-10-k-Filings

# Activate your Python virtual environment
source venv/bin/activate

# Run your Python script
python3 scrape_entire_text_mda.py

# Deactivate the virtual environment when done
deactivate
