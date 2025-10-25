./image_init.sh
./wait_result.sh $0 &
sbatch scripts/pipeline.sbatch
