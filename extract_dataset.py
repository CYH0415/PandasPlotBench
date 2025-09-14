#!/usr/bin/env python3
"""
提取dataset.parquet中指定列的前100项数据到JSON文件
"""

import pandas as pd
import json
import os


def extract_data_to_json():
    """
    从dataset.parquet文件中提取指定列的前100项数据并保存为JSON文件
    """
    # 定义输入文件路径
    parquet_file = "dataset/dataset.parquet"
    
    # 定义要提取的列
    columns_to_extract = [
        "id",
        "task__plot_description", 
        "task__plot_style",
        "_task__plot_description_short",
        "_task__plot_description_short_single"
    ]
    
    # 定义输出文件路径
    output_file = "extracted_data.json"
    
    try:
        # 检查输入文件是否存在
        if not os.path.exists(parquet_file):
            print(f"错误: 文件 {parquet_file} 不存在")
            return
        
        print(f"正在读取文件: {parquet_file}")
        
        # 读取parquet文件
        df = pd.read_parquet(parquet_file)
        
        print(f"数据集总行数: {len(df)}")
        print(f"数据集总列数: {len(df.columns)}")
        
        # 检查所需列是否存在
        missing_columns = [col for col in columns_to_extract if col not in df.columns]
        if missing_columns:
            print(f"警告: 以下列在数据集中不存在: {missing_columns}")
            print(f"数据集中可用的列: {list(df.columns)}")
            # 只提取存在的列
            columns_to_extract = [col for col in columns_to_extract if col in df.columns]
        
        if not columns_to_extract:
            print("错误: 没有可提取的列")
            return
        
        # 提取指定列的前100行
        extracted_data = df[columns_to_extract].head(100)
        
        print(f"提取了 {len(extracted_data)} 行数据，包含列: {columns_to_extract}")
        
        # 转换为JSON格式的字典列表
        data_list = extracted_data.to_dict('records')
        
        # 确保所有字符串类型的数据都正确处理
        for record in data_list:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, str):
                    record[key] = str(value)
                else:
                    record[key] = str(value) if value is not None else None
        
        # 保存为JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        
        print(f"数据已成功保存到: {output_file}")
        print(f"保存了 {len(data_list)} 条记录")
        
        # 显示前几条记录作为预览
        print("\n前3条记录预览:")
        for i, record in enumerate(data_list[:3]):
            print(f"\n记录 {i+1}:")
            for key, value in record.items():
                print(f"  {key}: {value}")
    
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    extract_data_to_json()
