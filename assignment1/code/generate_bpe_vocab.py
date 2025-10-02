import os
import sys
import subprocess

# 定义文件路径
input_file_en = '../output/preprocessed_text_en.txt'  # 英语输入文件
input_file_ha = '../output/preprocessed_text_ha.txt'  # 豪萨语输入文件
input_file_combined = '../output/preprocessed_text_combined.txt'  # 合并输入文件

# BPE模型和输出文件
bpe_model_file = '../output/bpe.model'
bpe_processed_file_en = '../output/bpe_processed_en.txt'  # 英语BPE处理文件
bpe_processed_file_ha = '../output/bpe_processed_ha.txt'  # 豪萨语BPE处理文件
vocab_file_en = '../output/bpe_vocab_en.txt'  # 英语词汇表
vocab_file_ha = '../output/bpe_vocab_ha.txt'  # 豪萨语词汇表

print(f"英语输入文件: {input_file_en}")
print(f"豪萨语输入文件: {input_file_ha}")
print(f"合并输入文件: {input_file_combined}")
print(f"BPE模型文件: {bpe_model_file}")
print(f"英语BPE处理文件: {bpe_processed_file_en}")
print(f"豪萨语BPE处理文件: {bpe_processed_file_ha}")
print(f"英语词汇表文件: {vocab_file_en}")
print(f"豪萨语词汇表文件: {vocab_file_ha}")

# 检查所有输入文件是否存在
for file_path in [input_file_en, input_file_ha, input_file_combined]:
    if not os.path.exists(file_path):
        print(f"错误: 输入文件 {file_path} 不存在")
        print("请先运行xml_to_text.py生成预处理后的文件")
        sys.exit(1)

# 步骤1: 在合并文本上学习BPE模型
print("\n步骤1: 在合并文本上学习BPE模型...")
try:
    # 使用subprocess调用正确路径的learn_bpe.py
    result = subprocess.run([
        'python', '../../subword-nmt/subword_nmt/learn_bpe.py', 
        '-s', '1000', 
        '--input', input_file_combined, 
        '--output', bpe_model_file
    ], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"警告: {result.stderr}")
    print(f"BPE模型已保存到 {bpe_model_file}")
except Exception as e:
    print(f"学习BPE模型失败: {e}")
    sys.exit(1)

# 检查BPE模型是否生成
if not os.path.exists(bpe_model_file):
    print(f"错误: BPE模型文件 {bpe_model_file} 未生成")
    sys.exit(1)

# 步骤2: 应用BPE模型处理英语文本
print("\n步骤2a: 应用BPE模型处理英语文本...")
try:
    # 使用subprocess调用apply_bpe.py
    with open(input_file_en, 'r', encoding='utf-8') as infile, open(bpe_processed_file_en, 'w', encoding='utf-8') as outfile:
        result = subprocess.run([
            'python', '../../subword-nmt/subword_nmt/apply_bpe.py', 
            '-c', bpe_model_file
        ], stdin=infile, stdout=outfile, stderr=subprocess.PIPE, text=True)
    if result.stderr:
        print(f"警告: {result.stderr}")
    print(f"英语BPE处理后的文本已保存到 {bpe_processed_file_en}")
except Exception as e:
    print(f"应用BPE模型到英语失败: {e}")
    sys.exit(1)

# 步骤2b: 应用BPE模型处理豪萨语文本
print("\n步骤2b: 应用BPE模型处理豪萨语文本...")
try:
    # 使用subprocess调用apply_bpe.py
    with open(input_file_ha, 'r', encoding='utf-8') as infile, open(bpe_processed_file_ha, 'w', encoding='utf-8') as outfile:
        result = subprocess.run([
            'python', '../../subword-nmt/subword_nmt/apply_bpe.py', 
            '-c', bpe_model_file
        ], stdin=infile, stdout=outfile, stderr=subprocess.PIPE, text=True)
    if result.stderr:
        print(f"警告: {result.stderr}")
    print(f"豪萨语BPE处理后的文本已保存到 {bpe_processed_file_ha}")
except Exception as e:
    print(f"应用BPE模型到豪萨语失败: {e}")
    sys.exit(1)

# 步骤3a: 生成英语BPE词汇表
print("\n步骤3a: 生成英语BPE词汇表...")
try:
    # 使用subprocess调用get_vocab.py
    with open(bpe_processed_file_en, 'r', encoding='utf-8') as infile, open(vocab_file_en, 'w', encoding='utf-8') as outfile:
        result = subprocess.run([
            'python', '../../subword-nmt/subword_nmt/get_vocab.py'
        ], stdin=infile, stdout=outfile, stderr=subprocess.PIPE, text=True)
    if result.stderr:
        print(f"警告: {result.stderr}")
    print(f"英语BPE词汇表已保存到 {vocab_file_en}")
except Exception as e:
    print(f"生成英语词汇表失败: {e}")
    sys.exit(1)

# 步骤3b: 生成豪萨语BPE词汇表
print("\n步骤3b: 生成豪萨语BPE词汇表...")
try:
    # 使用subprocess调用get_vocab.py
    with open(bpe_processed_file_ha, 'r', encoding='utf-8') as infile, open(vocab_file_ha, 'w', encoding='utf-8') as outfile:
        result = subprocess.run([
            'python', '../../subword-nmt/subword_nmt/get_vocab.py'
        ], stdin=infile, stdout=outfile, stderr=subprocess.PIPE, text=True)
    if result.stderr:
        print(f"警告: {result.stderr}")
    print(f"豪萨语BPE词汇表已保存到 {vocab_file_ha}")
except Exception as e:
    print(f"生成豪萨语词汇表失败: {e}")
    sys.exit(1)

# 检查词汇表文件是否生成
for file_path in [vocab_file_en, vocab_file_ha]:
    if not os.path.exists(file_path):
        print(f"错误: 词汇表文件 {file_path} 未生成")
        sys.exit(1)

print("\nBPE词汇表生成完成！")

# 显示每种语言词汇表的前几个条目
for lang_name, vocab_path in [("英语", vocab_file_en), ("豪萨语", vocab_file_ha)]:
    print(f"\n{lang_name}词汇表前10个条目:")
    try:
        with open(vocab_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < 10:
                    print(line.strip())
                else:
                    break
        print("...")
    except Exception as e:
        print(f"读取{lang_name}词汇表失败: {e}")

# 计算词汇表大小
for lang_name, vocab_path in [("英语", vocab_file_en), ("豪萨语", vocab_file_ha)]:
    try:
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab_size = sum(1 for _ in f)
        print(f"{lang_name}词汇表大小: {vocab_size} 个标记")
    except Exception as e:
        print(f"计算{lang_name}词汇表大小失败: {e}")