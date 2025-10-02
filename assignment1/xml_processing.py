import xml.etree.ElementTree as ET
import re
import os
import subprocess
import tempfile


def xml_to_plain_text(xml_content):
    """
    将XML内容转换为基于行的纯文本
    要求：移除所有标点符号，转换为小写
    """
    try:
        # 解析XML
        root = ET.fromstring(xml_content)
        
        # 提取所有文本内容
        all_text = []
        
        def extract_text(element):
            # 获取当前元素的文本
            if element.text:
                all_text.append(element.text)
            # 递归处理子元素
            for child in element:
                extract_text(child)
                # 处理子元素的尾部文本
                if child.tail:
                    all_text.append(child.tail)
        
        extract_text(root)
        
        # 合并所有文本
        full_text = ' '.join(all_text)
        
        # 移除标点符号
        full_text = re.sub(r'[\p{P}\p{S}]', ' ', full_text, flags=re.UNICODE)
        # 如果上面的Unicode正则不工作，使用备用方法
        if not re.search(r'\p{P}', '', flags=re.UNICODE):  # 检查是否支持Unicode属性
            full_text = re.sub(r'[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', ' ', full_text)
        
        # 转换为小写
        full_text = full_text.lower()
        
        # 移除多余的空白字符
        full_text = re.sub(r'\s+', ' ', full_text).strip()
        
        # 按行分割（这里我们简单地按句号分割，然后清理）
        sentences = re.split(r'\.', full_text)
        # 过滤掉空行
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        
        return sentences
        
    except ET.ParseError as e:
        print(f"XML解析错误: {e}")
        # 如果XML解析失败，尝试直接处理文本
        text = xml_content
        # 移除XML标签
        text = re.sub(r'<[^>]+>', ' ', text)
        # 移除标点符号
        text = re.sub(r'[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', ' ', text)
        # 转换为小写
        text = text.lower()
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text).strip()
        # 分割成行
        sentences = re.split(r'\.', text)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        return sentences
    except Exception as e:
        print(f"处理XML时出错: {e}")
        return []


def download_sample_xml():
    """
    下载示例XML文件
    """
    sample_xml_url = "https://raw.githubusercontent.com/wmt-conference/wmt-format-tools/main/test/sample-data/sample-hyp.xml"
    try:
        import requests
        print(f"正在下载示例XML文件: {sample_xml_url}")
        response = requests.get(sample_xml_url)
        response.raise_for_status()
        return response.text
    except ImportError:
        print("requests库未安装，使用示例XML内容")
        # 提供一个简单的示例XML内容作为备选
        sample_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<mteval>
  <srcset setid="newstest2014" srclang="en">
    <doc docid="1000">
      <seg id="1">Hello world! This is a test.</seg>
      <seg id="2">Data engineering is interesting, right?</seg>
    </doc>
  </srcset>
</mteval>'''
        return sample_xml
    except Exception as e:
        print(f"下载失败: {e}")
        # 返回示例内容
        sample_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<mteval>
  <srcset setid="newstest2014" srclang="en">
    <doc docid="1000">
      <seg id="1">Hello world! This is a test.</seg>
      <seg id="2">Data engineering is interesting, right?</seg>
    </doc>
  </srcset>
</mteval>'''
        return sample_xml


def install_subword_nmt():
    """
    安装subword-nmt工具
    """
    try:
        print("检查subword-nmt是否已安装...")
        # 尝试导入subword-nmt
        import subword_nmt
        print("subword-nmt已安装")
        return True
    except ImportError:
        print("正在安装subword-nmt...")
        try:
            subprocess.run(["pip", "install", "subword-nmt"], check=True)
            print("subword-nmt安装成功")
            return True
        except Exception as e:
            print(f"subword-nmt安装失败: {e}")
            return False


def build_bpe_vocabulary(text_lines, vocab_size=1000):
    """
    构建BPE词汇表
    """
    if not text_lines:
        print("没有文本数据用于构建BPE词汇表")
        return []
    
    # 检查subword-nmt是否可用
    if not install_subword_nmt():
        print("无法继续构建BPE词汇表")
        return []
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # 保存文本到临时文件
            input_file = os.path.join(temp_dir, "input.txt")
            with open(input_file, "w", encoding="utf-8") as f:
                for line in text_lines:
                    f.write(line + "\n")
            
            # 学习BPE编码
            codes_file = os.path.join(temp_dir, "bpe_codes")
            subprocess.run(
                ["subword-nmt", "learn-bpe", "-s", str(vocab_size), "--input", input_file, "--output", codes_file],
                check=True
            )
            
            # 应用BPE编码获取词汇表
            vocab_file = os.path.join(temp_dir, "vocabulary.txt")
            subprocess.run(
                ["subword-nmt", "apply-bpe", "--codes", codes_file, "--input", input_file, "--output", vocab_file],
                check=True
            )
            
            # 提取词汇表
            vocabulary = set()
            with open(vocab_file, "r", encoding="utf-8") as f:
                for line in f:
                    tokens = line.strip().split()
                    vocabulary.update(tokens)
            
            # 转换为列表并排序
            return sorted(list(vocabulary))
            
    except subprocess.CalledProcessError as e:
        print(f"BPE处理失败: {e}")
        # 如果subword-nmt失败，返回简单的词汇表
        simple_vocab = set()
        for line in text_lines:
            simple_vocab.update(line.split())
        return sorted(list(simple_vocab))
    except Exception as e:
        print(f"构建BPE词汇表时出错: {e}")
        return []


def main():
    """
    主函数：处理XML并构建BPE词汇表
    """
    # 创建输出目录
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 下载或获取示例XML
    xml_content = download_sample_xml()
    
    # 转换XML为纯文本
    plain_text_lines = xml_to_plain_text(xml_content)
    
    # 保存处理后的文本
    output_file = os.path.join(output_dir, "plain_text_output.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for line in plain_text_lines:
            f.write(line + "\n")
    
    print(f"\n已将XML转换为纯文本并保存到: {output_file}")
    print("\n处理后的文本内容预览:")
    for i, line in enumerate(plain_text_lines[:3]):
        print(f"第{i+1}行: {line}")
    
    # 构建BPE词汇表
    print("\n开始构建BPE词汇表...")
    vocabulary = build_bpe_vocabulary(plain_text_lines)
    
    # 保存词汇表
    vocab_output_file = os.path.join(output_dir, "bpe_vocabulary.txt")
    with open(vocab_output_file, "w", encoding="utf-8") as f:
        for token in vocabulary:
            f.write(token + "\n")
    
    print(f"\nBPE词汇表已保存到: {vocab_output_file}")
    print(f"词汇表大小: {len(vocabulary)}")
    print("\n词汇表前10个标记:")
    for token in vocabulary[:10]:
        print(f"- {token}")


if __name__ == "__main__":
    main()