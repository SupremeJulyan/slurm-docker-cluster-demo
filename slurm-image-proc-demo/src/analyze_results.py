import json
import numpy as np
import pandas as pd

def analyze_features(csv_path, output_json):
    df = pd.read_csv(csv_path)
    
    # 计算平均特征向量
    features = df.iloc[:, 1:].values
    avg_features = np.mean(features, axis=0).tolist()
    
    # 计算特征范围
    min_features = np.min(features, axis=0).tolist()
    max_features = np.max(features, axis=0).tolist()
    
    # 保存结果
    result = {
        "total_images": len(df),
        "avg_features": avg_features,
        "feature_range": {
            "min": min_features,
            "max": max_features
        }
    }
    
    with open(output_json, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"分析完成! 结果保存至 {output_json}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("用法: python analyze_results.py <输入CSV> <输出JSON>")
        sys.exit(1)
    
    analyze_features(sys.argv[1], sys.argv[2])