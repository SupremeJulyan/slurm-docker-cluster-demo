./image_init.sh
#./wait_result.sh $0 &
# 运行转换脚本
/data/conda/envs/image_proc/bin/python src/convert_format.py data/source/
# 运行缩放脚本
/data/conda/envs/image_proc/bin/python src/resize_images.py data/png/ 512x512
# 运行提取特征脚本
module load mpi/openmpi-x86_64
mpirun --allow-run-as-root -np 4 /data/conda/envs/image_proc/bin/python src/extract_features.py data/resize results/features.csv
# 运行分析特征脚本
/data/conda/envs/image_proc/bin/python src/analyze_results.py results/features.csv results/summary.json
