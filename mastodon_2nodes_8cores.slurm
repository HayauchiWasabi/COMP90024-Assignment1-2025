#!/bin/bash

#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --time=0-01:00:00
#SBATCH --mem=90G
#SBATCH --output=output_%j.txt
#SBATCH --error=error_%j.txt

module purge
module load foss/2022a
module load Python/3.10.4
module load mpi4py/3.1.4

srun -n 8 python3 mastodon_analysis_v4.py mastodon-144g.ndjson

my-job-stats -a -n -s