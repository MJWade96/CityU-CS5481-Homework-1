# 创建 BPE 词汇表的步骤

要使用 `subword-nmt` 工具创建 BPE 词汇表（按行保存每个 BPE  token），可按照以下步骤操作：

### 步骤 1：学习 BPE 合并规则（codes）并生成词汇表

使用 `learn-joint-bpe-and-vocab` 命令可同时学习 BPE 合并规则并为每种语言生成词汇表（推荐用于双语 / 多语场景）。该命令会自动将 BPE  token 及其频率按行保存到指定文件中。

#### 命令示例：



```
subword-nmt learn-joint-bpe-and-vocab \\

&#x20;   \--input train.L1 train.L2 \  # 输入训练文件（支持多个，如双语语料）

&#x20;   -s 10000 \  # BPE 合并操作的数量（生成的子词数量相关）

&#x20;   -o bpe.codes \  # 输出的 BPE 合并规则文件

&#x20;   \--write-vocabulary vocab.L1 vocab.L2  # 输出的词汇表文件（每个输入文件对应一个）
```



* **参数说明**：


  * `--input`：训练语料文件（如 `train.en` 和 `train.zh` 对应英中双语）。

  * `-s`：BPE 合并操作的数量，决定最终子词表的大小（值越大，子词越长）。

  * `-o`：保存 BPE 合并规则的文件（后续用于应用 BPE）。

  * `--write-vocabulary`：指定输出的词汇表文件，每个输入文件对应一个（如 `vocab.en` 和 `vocab.zh`）。

### 步骤 2：词汇表文件格式说明

生成的词汇表文件（如 `vocab.L1`）中，每行包含一个 BPE  token 及其在训练语料中的频率，格式为：



```
token1 1000

token2 500

...
```

其中第一列即为 BPE  token，按行存储，可直接用于后续的模型训练或其他需求。

### 步骤 3：（可选）单独提取词汇表

如果已通过 `learn-bpe` 生成了 BPE 合并规则（`bpe.codes`），可通过以下步骤单独提取词汇表：



1. 先将 BPE 应用到训练文件：



```
subword-nmt apply-bpe -c bpe.codes < train.L1 > train.BPE.L1
```



1. 从 BPE 处理后的文件中提取词汇表：



```
subword-nmt get-vocab < train.BPE.L1 > vocab.L1
```

生成的 `vocab.L1` 格式与步骤 1 相同，每行一个 BPE  token。

### 总结

通过 `learn-joint-bpe-and-vocab` 命令可一步完成 BPE 规则学习和词汇表生成，生成的词汇表文件直接按行保存 BPE  token，无需额外处理。如需单独生成，可结合 `apply-bpe` 和 `get-vocab` 命令。

> （注：文档部分内容可能由 AI 生成）