#!/bin/bash
#SBATCH --job-name=img_features
#SBATCH --output=logs/features_%j.out
#SBATCH --error=logs/features_%j.err
#SBATCH --nodes=1                  # 使用1个节点
#SBATCH --ntasks-per-node=2        # 每个节点4个进程
#SBATCH --cpus-per-task=1
#SBATCH --time=00:20:00
#SBATCH --partition=normal

source activate image_proc
# 运行提取特征脚本
mpirun --allow-run-as-root -np $SLURM_NTASKS python src/extract_features.py data/resize results/features.csv
