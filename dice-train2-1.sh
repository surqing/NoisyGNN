#!/bin/bash

# 定义模型、数据集和参数
modelnames=("GCN")
datasets=("polblogs")
seeds=("15" "1000" "4000")
ptb_rates=("0" "0.05" "0.1")

# 循环遍历所有组合
for model in "${modelnames[@]}"; do
  for dataset in "${datasets[@]}"; do
    for seed in "${seeds[@]}"; do
      for ptb_rate in "${ptb_rates[@]}"; do
        # 构建命令
        cmd="python main_dice.py --seed $seed --dataset $dataset --ptb_rate $ptb_rate"
        
        # 提示训练开始
        echo "Starting training with parameters: dataset=$dataset, seed=$seed, ptb_rate=$ptb_rate"
        
        # 执行命令并进行错误处理
        if $cmd; then
          echo "Training completed successfully for parameters: dataset=$dataset, seed=$seed, ptb_rate=$ptb_rate"
        else
          echo "Error occurred during training for parameters: dataset=$dataset, seed=$seed, ptb_rate=$ptb_rate" >&2
        fi
      done
    done
  done
done
