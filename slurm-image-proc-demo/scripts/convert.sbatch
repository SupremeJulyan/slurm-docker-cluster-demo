#!/bin/bash
#SBATCH --job-name=img_convert
#SBATCH --output=logs/convert_%j.out
#SBATCH --error=logs/convert_%j.err
#SBATCH --ntasks=1
#SBATCH --time=00:10:00
#SBATCH --partition=normal


source activate image_proc
# 运行转换脚本
python src/convert_format.py data/source/
