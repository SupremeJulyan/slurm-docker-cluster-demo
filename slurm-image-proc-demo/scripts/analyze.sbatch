#!/bin/bash
#SBATCH --job-name=img_analyze
#SBATCH --output=logs/analyze_%j.out
#SBATCH --error=logs/analyze_%j.err
#SBATCH --ntasks=1
#SBATCH --time=00:10:00
#SBATCH --partition=normal

source activate image_proc
# 运行分析特征脚本
python src/analyze_results.py results/features.csv results/summary.json
