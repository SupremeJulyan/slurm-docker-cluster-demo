#!/bin/bash

file="results/summary.json"
start_time=$(date +%s.%N)  # 使用高精度时间

echo "Monitoring started at $(date)"
echo "Waiting for file creation: $file"

# 等待文件创建
while [ ! -f "$file" ]; do
    sleep 0.1  # 更频繁的检查
done

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)

echo "$1 Cost $duration seconds" >> time.txt