import base64
import glob
import os
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches
from omegaconf import OmegaConf

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
print(parent_dir)
from plotting_benchmark.vis_generator import read_responses


def decode_image(encoded_image, output_image_file):
    decoded_image = base64.b64decode(encoded_image)

    # Write the decoded image data to a file
    with open(output_image_file, "wb") as image_file:
        image_file.write(decoded_image)


"""
Just a script to generate a docx file to dump generated tasks and plots to verify them.
"""
do_random = False
# suffix = "_probs"
suffix = ""
if do_random and len(suffix) == 0:
    suffix = "_random"

# config_path = "../configs/config.yaml"
config_path = "configs/config.yaml"
config = OmegaConf.load(config_path)
paths = config.paths

dataset_folder = Path(paths.dataset_folder)
results_folder = Path(paths.out_folder)
temp_folder = results_folder / "temp"
os.makedirs(temp_folder, exist_ok=True)
# 自动查找最新的结果文件
bench_files = list(results_folder.glob("benchmark_stat*.jsonl"))
result_files = list(results_folder.glob("results_*.json"))

if not bench_files:
    raise FileNotFoundError("No benchmark_stat*.jsonl files found in output folder")
if not result_files:
    raise FileNotFoundError("No results_*.json files found in output folder")

# 使用最新的文件
bench_file = sorted(bench_files, key=os.path.getmtime)[-1]
response_file = sorted(result_files, key=os.path.getmtime)[-1]

print(f"Using benchmark file: {bench_file}")
print(f"Using results file: {response_file}")

# 读取结果文件（pandas JSON格式）
import json
with open(response_file, 'r', encoding='utf-8') as f:
    plot_data = json.load(f)

# 将pandas JSON格式转换为标准格式
plot_responses = {}
if 'id' in plot_data:
    for i, idx in plot_data['id'].items():
        entry = {'id': idx}
        for key, values in plot_data.items():
            if key != 'id':
                entry[key] = values[i]
        plot_responses[idx] = entry

print(f"Found {len(plot_responses)} responses")
print(f"Sample IDs: {list(plot_responses.keys())[:3]}")

temp_image_file = temp_folder / "plot.png"

# 使用结果文件中的ID列表
ids = list(plot_responses.keys())

doc = Document()
section = doc.sections[0]
new_width, new_height = section.page_height, section.page_width
section.page_width = new_width
section.page_height = new_height

for idx in ids:
    response = plot_responses[idx]
    
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    paragraph.add_run(f"ID = {idx}\n")
    
    # 从response中获取分数信息
    if 'score_vis' in response:
        vis_score = response['score_vis']
        paragraph.add_run(f"Vis Score = {vis_score}\n")
    if 'score_task' in response:
        task_score = response['score_task']
        paragraph.add_run(f"Task Score = {task_score}\n")
    if 'has_plot' in response:
        has_plot = response['has_plot']
        paragraph.add_run(f"Has Plot = {has_plot}\n")

    dp_folder = dataset_folder / str(idx)

    # 查找对应的真实图片
    plot_files = glob.glob(os.path.join(str(dp_folder), "*.png"))
    
    if not plot_files:
        paragraph.add_run(f"Warning: No ground truth image found for ID {idx}\n")
        doc.add_page_break()
        continue
    
    plot_file = plot_files[0]

    if len(plot_files) > 1:
        paragraph.add_run(
            f"Note: Found {len(plot_files)} images in GT, using the first one\n"
        )

    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"

    cell = table.cell(0, 0)
    cell.text = "Generated"

    # 检查生成的图像
    if 'plot_b64' in response and response['plot_b64']:
        try:
            decode_image(response['plot_b64'], temp_image_file)
            paragraph = cell.paragraphs[0]
            run = paragraph.add_run()
            run.add_picture(str(temp_image_file), width=Inches(4))
        except Exception as e:
            cell.text = f"Generated\nError decoding image: {str(e)}"
    else:
        cell.text = "Generated\nNo image generated"

    cell = table.cell(0, 1)
    cell.text = "Ground truth"
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run()
    run.add_picture(plot_file, width=Inches(4))

    doc.add_page_break()

result_file = results_folder / "bench_results.docx"
doc.save(result_file)
print(f"Output saved in {str(result_file)}")
