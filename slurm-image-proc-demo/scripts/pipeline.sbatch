#!/bin/bash
#SBATCH --job-name=img_pipeline
#SBATCH --output=logs/pipeline_%j.out
#SBATCH --error=logs/pipeline_%j.err
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --partition=normal

# 步骤1: 格式转换,--parsable可获取job id
JOB1=$(sbatch --parsable scripts/convert.sbatch)

# 步骤2: 图像缩放 (依赖步骤1)
JOB2=$(sbatch --depend=afterok:$JOB1 --parsable scripts/resize.sbatch)

# 步骤3: 特征提取 (依赖步骤2)
JOB3=$(sbatch --depend=afterok:$JOB2 --parsable scripts/features.sbatch)

# 步骤4: 结果分析 (依赖步骤3)
sbatch --depend=afterok:$JOB3 scripts/analyze.sbatch
