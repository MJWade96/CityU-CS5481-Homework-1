@echo off

REM 学习BPE模型
python ..\..\subword-nmt\learn_bpe.py -s 1000 --input ..\output\preprocessed_text.txt --output ..\output\bpe.model

echo BPE模型学习完成，正在应用模型生成词汇表...

REM 应用BPE模型并生成词汇表
python ..\..\subword-nmt\get_vocab.py < ..\output\preprocessed_text.txt > ..\output\vocab.txt

REM 使用BPE模型处理文本
python ..\..\subword-nmt\apply_bpe.py -c ..\output\bpe.model < ..\output\preprocessed_text.txt > ..\output\bpe_processed.txt

echo 处理完成！