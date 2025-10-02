import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random
from scipy import spatial

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号


def generate_student_data(num_students=500):
    """
    生成500名学生的随机数据
    """
    np.random.seed(42)  # 设置随机种子以确保结果可复现
    
    # 生成学生ID
    student_ids = list(range(1, num_students + 1))
    
    # 生成专业 (Computer Science, Mathematics, Physics)
    majors = ['Computer Science', 'Mathematics', 'Physics']
    major_distribution = [0.4, 0.35, 0.25]  # 各专业的分布比例
    student_majors = np.random.choice(majors, size=num_students, p=major_distribution)
    
    # 生成性别 (Male, Female)
    genders = ['Male', 'Female']
    gender_distribution = [0.52, 0.48]  # 性别的分布比例
    student_genders = np.random.choice(genders, size=num_students, p=gender_distribution)
    
    # 生成GPA (0.0-4.0)，根据专业设置不同的分布
    gpas = []
    for major in student_majors:
        if major == 'Computer Science':
            # CS专业的GPA稍微高一点
            gpa = max(0.0, min(4.0, np.random.normal(3.2, 0.5)))
        elif major == 'Mathematics':
            # Math专业的GPA中等
            gpa = max(0.0, min(4.0, np.random.normal(3.0, 0.6)))
        else:  # Physics
            # Physics专业的GPA稍低
            gpa = max(0.0, min(4.0, np.random.normal(2.9, 0.7)))
        gpas.append(round(gpa, 2))
    
    # 创建DataFrame
    df = pd.DataFrame({
        'Student ID': student_ids,
        'Major': student_majors,
        'Gender': student_genders,
        'GPA': gpas
    })
    
    return df


def visualize_distributions(df):
    """
    可视化每个属性的分布
    """
    plt.figure(figsize=(15, 12))
    
    # 1. GPA分布 - 直方图
    plt.subplot(2, 2, 1)
    sns.histplot(df['GPA'], kde=True, bins=20)
    plt.title('GPA分布')
    plt.xlabel('GPA')
    plt.ylabel('频数')
    plt.grid(True, alpha=0.3)
    
    # 2. 专业分布 - 饼图
    plt.subplot(2, 2, 2)
    major_counts = df['Major'].value_counts()
    plt.pie(major_counts.values, labels=major_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('专业分布')
    plt.axis('equal')  # 使饼图为正圆形
    
    # 3. 性别分布 - 柱状图
    plt.subplot(2, 2, 3)
    gender_counts = df['Gender'].value_counts()
    sns.barplot(x=gender_counts.index, y=gender_counts.values)
    plt.title('性别分布')
    plt.xlabel('性别')
    plt.ylabel('人数')
    plt.grid(True, alpha=0.3, axis='y')
    
    # 4. 各专业的GPA分布 - 箱线图
    plt.subplot(2, 2, 4)
    sns.boxplot(x='Major', y='GPA', data=df)
    plt.title('各专业GPA分布')
    plt.xlabel('专业')
    plt.ylabel('GPA')
    plt.xticks(rotation=15)
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return plt


def visualize_relationships(df):
    """
    可视化属性之间的关系
    """
    plt.figure(figsize=(15, 10))
    
    # 1. 专业和性别的交叉分析 - 分组柱状图
    plt.subplot(2, 2, 1)
    cross_tab = pd.crosstab(df['Major'], df['Gender'])
    cross_tab.plot(kind='bar', ax=plt.gca())
    plt.title('各专业性别分布')
    plt.xlabel('专业')
    plt.ylabel('人数')
    plt.xticks(rotation=15)
    plt.legend(title='性别')
    plt.grid(True, alpha=0.3, axis='y')
    
    # 2. 性别与GPA的关系 - 小提琴图
    plt.subplot(2, 2, 2)
    sns.violinplot(x='Gender', y='GPA', data=df)
    plt.title('性别与GPA的关系')
    plt.xlabel('性别')
    plt.ylabel('GPA')
    plt.grid(True, alpha=0.3, axis='y')
    
    # 3. 各专业平均GPA - 柱状图
    plt.subplot(2, 2, 3)
    avg_gpa_by_major = df.groupby('Major')['GPA'].mean().sort_values(ascending=False)
    sns.barplot(x=avg_gpa_by_major.index, y=avg_gpa_by_major.values)
    plt.title('各专业平均GPA')
    plt.xlabel('专业')
    plt.ylabel('平均GPA')
    plt.xticks(rotation=15)
    plt.grid(True, alpha=0.3, axis='y')
    
    # 4. GPA分布按专业和性别 - 分组直方图
    plt.subplot(2, 2, 4)
    sns.histplot(data=df, x='GPA', hue='Major', multiple='stack', bins=15)
    plt.title('GPA分布按专业')
    plt.xlabel('GPA')
    plt.ylabel('频数')
    plt.legend(title='专业')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return plt


def plot_students_per_major(df):
    """
    计算各专业学生数量并绘制柱状图
    """
    # 计算各专业学生数量
    major_counts = df['Major'].value_counts()
    
    # 绘制柱状图
    plt.figure(figsize=(10, 6))
    bars = plt.bar(major_counts.index, major_counts.values, color=['#3498db', '#e74c3c', '#2ecc71'])
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.title('各专业学生数量')
    plt.xlabel('专业')
    plt.ylabel('学生数量')
    plt.xticks(rotation=15)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    return plt, major_counts


def compute_and_visualize_similarity():
    """
    计算并可视化用户和物品嵌入的相似度热图
    """
    # 设置随机种子
    np.random.seed(42)
    
    # 随机初始化用户和物品嵌入
    d = 8  # 嵌入维度
    U = np.random.randn(5, d)  # 用户嵌入 (5×8)
    V = np.random.randn(5, d)  # 物品嵌入 (5×8)
    
    # 计算相似度矩阵
    # 首先计算点积矩阵
    dot_product = np.dot(U, V.T)
    
    # 归一化（除以sqrt(d)）
    normalized_dot = dot_product / np.sqrt(d)
    
    # 应用softmax函数
    similarity_matrix = np.exp(normalized_dot) / np.sum(np.exp(normalized_dot), axis=1, keepdims=True)
    
    # 可视化热图
    plt.figure(figsize=(10, 8))
    
    # 创建热图
    sns.heatmap(similarity_matrix, annot=True, cmap='viridis', fmt='.3f',
                xticklabels=[f'Item {i+1}' for i in range(5)],
                yticklabels=[f'User {i+1}' for i in range(5)])
    
    plt.title('用户-物品相似度矩阵 (Softmax归一化)')
    plt.xlabel('物品')
    plt.ylabel('用户')
    plt.tight_layout()
    
    return plt, similarity_matrix, U, V


def main():
    """
    主函数：运行所有可视化任务
    """
    # 创建输出目录
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("\n=== Part (b): 生成500名学生数据并可视化属性分布 ===")
    # 生成学生数据
    student_df = generate_student_data(500)
    print(f"生成了{len(student_df)}名学生的数据")
    
    # 显示数据预览
    print("\n学生数据预览:")
    print(student_df.head())
    
    # 可视化属性分布
    dist_fig = visualize_distributions(student_df)
    dist_fig.savefig(os.path.join(output_dir, 'attribute_distributions.png'), dpi=300, bbox_inches='tight')
    print("\n属性分布图已保存")
    
    print("\n=== 属性分布可视化说明 ===")
    print("1. GPA分布直方图: 显示了GPA的整体分布情况，可以观察到成绩集中在哪个区间")
    print("2. 专业分布饼图: 直观展示了三个专业的学生比例")
    print("3. 性别分布柱状图: 显示了男女学生的数量对比")
    print("4. 各专业GPA分布箱线图: 展示了不同专业GPA的分布特征和异常值")
    
    # 可视化属性关系
    rel_fig = visualize_relationships(student_df)
    rel_fig.savefig(os.path.join(output_dir, 'attribute_relationships.png'), dpi=300, bbox_inches='tight')
    print("\n属性关系图已保存")
    
    print("\n=== 属性关系可视化说明 ===")
    print("1. 各专业性别分布: 展示了每个专业中男女生的分布情况")
    print("2. 性别与GPA关系: 通过小提琴图展示了不同性别学生的GPA分布")
    print("3. 各专业平均GPA: 直观对比了三个专业的平均成绩水平")
    print("4. GPA分布按专业: 展示了不同专业学生的GPA分布叠加情况")
    
    print("\n=== Part (c): 各专业学生数量统计 ===")
    # 绘制各专业学生数量柱状图
    major_fig, major_counts = plot_students_per_major(student_df)
    major_fig.savefig(os.path.join(output_dir, 'students_per_major.png'), dpi=300, bbox_inches='tight')
    
    print("\n各专业学生数量:")
    for major, count in major_counts.items():
        print(f"- {major}: {count}人")
    
    print("\n=== Part (d): 用户-物品相似度计算与可视化 ===")
    # 计算并可视化相似度矩阵
    sim_fig, similarity_matrix, U, V = compute_and_visualize_similarity()
    sim_fig.savefig(os.path.join(output_dir, 'user_item_similarity.png'), dpi=300, bbox_inches='tight')
    
    print("\n相似度矩阵已计算并可视化")
    print("\n相似度矩阵预览:")
    print(np.round(similarity_matrix, 3))
    
    print("\n=== 所有可视化图表已保存到output目录 ===")
    print(f"输出目录: {output_dir}")
    
    # 显示一些统计信息
    print("\n=== 数据统计摘要 ===")
    print("\nGPA统计:")
    print(student_df['GPA'].describe())
    
    print("\n专业分布:")
    print(student_df['Major'].value_counts(normalize=True).apply(lambda x: f"{x:.2%}"))
    
    print("\n性别分布:")
    print(student_df['Gender'].value_counts(normalize=True).apply(lambda x: f"{x:.2%}"))


if __name__ == "__main__":
    main()