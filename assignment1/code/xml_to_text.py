import xml.etree.ElementTree as ET
import re
import os

# 定义输入和输出文件路径
input_file = '../data/sample-hyp.xml'
output_file_en = '../output/preprocessed_text_en.txt'  # 英语输出文件
output_file_ha = '../output/preprocessed_text_ha.txt'  # 豪萨语输出文件
output_file_combined = '../output/preprocessed_text_combined.txt'  # 合并输出文件

# 确保输出目录存在
os.makedirs(os.path.dirname(output_file_en), exist_ok=True)

def preprocess_text(text):
    # 转换为小写
    text = text.lower()
    # 移除所有标点符号和多余的空格
    text = re.sub(r'[\W]+', ' ', text)
    # 移除多余的空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    # 解析XML文件
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # 打开输出文件
    with open(output_file_en, 'w', encoding='utf-8') as en_file, \
         open(output_file_ha, 'w', encoding='utf-8') as ha_file, \
         open(output_file_combined, 'w', encoding='utf-8') as combined_file:
        
        # 遍历所有文档
        en_count = 0
        ha_count = 0
        
        for doc in root.findall('./doc'):
            # 提取英语原文
            en_segs = doc.findall('.//src[@lang="en"]//seg')
            for seg in en_segs:
                if seg.text:
                    processed_text = preprocess_text(seg.text)
                    en_file.write(processed_text + '\n')
                    combined_file.write(processed_text + '\n')
                    en_count += 1
            
            # 提取豪萨语译文
            ha_segs = doc.findall('.//hyp[@system="MT"][@language="ha"]//seg')
            for seg in ha_segs:
                if seg.text:
                    processed_text = preprocess_text(seg.text)
                    ha_file.write(processed_text + '\n')
                    combined_file.write(processed_text + '\n')
                    ha_count += 1
    
    print(f'预处理完成！')
    print(f'英语原文保存在 {output_file_en}，共 {en_count} 行')
    print(f'豪萨语译文保存在 {output_file_ha}，共 {ha_count} 行')
    print(f'合并文本保存在 {output_file_combined}')
    print('\n注意：此数据集包含英语(en)和豪萨语(ha)两种语言，')
    print('建议使用subword-nmt的联合BPE学习方法，在合并文本上学习BPE模型，')
    print('然后分别应用于两种语言并生成各自的词汇表。')

if __name__ == '__main__':
    main()