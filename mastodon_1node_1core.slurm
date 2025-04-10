#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=190G
#SBATCH --time=0-01:00:00
#SBATCH --output=output_%j.txt
#SBATCH --error=error_%j.txt

module purge
module load foss/2022a
module load Python/3.10.4
module load mpi4py/3.1.4

srun -n 1 python3 mastodon_analysis_v4.py mastodon-144g.ndjson

my-job-stats -a -n -s