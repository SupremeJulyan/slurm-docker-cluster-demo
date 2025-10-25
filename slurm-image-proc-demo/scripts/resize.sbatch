#!/bin/bash
#SBATCH --job-name=img_resize
#SBATCH --output=logs/resize_%A_%a.out  # %A=作业ID, %a=任务ID
#SBATCH --error=logs/resize_%A_%a.err
#SBATCH --array=0-3  # 创建4个并行任务
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2  # 每个任务使用2个CPU核心
#SBATCH --time=00:15:00
#SBATCH --partition=normal

source activate image_proc
# 运行缩放脚本
python src/resize_images.py data/png/ 512x512
