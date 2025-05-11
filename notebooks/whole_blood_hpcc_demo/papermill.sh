#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32         # Try 16–32 if available
#SBATCH --mem=64G                  # 32 GB is a good start
#SBATCH --time=24:00:00
#SBATCH --job-name=wb
#SBATCH --output=wb_%j.out
#SBATCH --error=wb_%j.err
#SBATCH --mail-user=xiaoqial@ucr.edu
#SBATCH --mail-type=ALL
#SBATCH -p epyc # You can use any of the following; epyc, intel, batch, highmem, gpu

# Add local bin to PATH
export PATH=$HOME/.local/bin:$PATH

module load anaconda

papermill gtex_whole_blood_XL.ipynb Output_XL.ipynb -k python3