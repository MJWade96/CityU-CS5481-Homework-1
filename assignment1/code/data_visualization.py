import numpy as np
import pandas as pd
import matplotlib

# 使用非交互式后端，避免显示问题
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 设置随机种子以确保结果可复现
np.random.seed(42)

class StudentDataVisualizer:
    def __init__(self):
        # 准备可视化环境
        plt.style.use('seaborn-v0_8')
        self.students_df = None
        self.user_embeddings = None
        self.item_embeddings = None
        self.similarity_matrix = None
    
    def generate_student_data(self):
        """
        生成500名学生的随机数据，包括Student ID、Major、Gender和GPA
        """
        # 生成学生ID
        student_ids = np.arange(1, 501)
        
        # 随机生成专业分布
        majors = ['Computer Science', 'Mathematics', 'Physics']
        major_distribution = [0.5, 0.3, 0.2]  # 专业分布比例
        student_majors = np.random.choice(majors, size=500, p=major_distribution)
        
        # 随机生成性别分布
        genders = ['Male', 'Female']
        gender_distribution = [0.52, 0.48]  # 性别分布比例
        student_genders = np.random.choice(genders, size=500, p=gender_distribution)
        
        # 生成GPA数据（正态分布，均值3.0，标准差0.5，限制在0-4之间）
        gpas = np.clip(np.random.normal(3.0, 0.5, size=500), 0, 4)
        
        # 创建DataFrame
        self.students_df = pd.DataFrame({
            'Student ID': student_ids,
            'Major': student_majors,
            'Gender': student_genders,
            'GPA': gpas
        })
        
        print("Student data generated.")
        return self.students_df
    
    def visualize_attribute_distributions(self):
        """
        可视化每个属性的分布
        """
        if self.students_df is None:
            self.generate_student_data()
        
        # 创建一个2x2的子图
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. 专业分布 - 饼图
        major_counts = self.students_df['Major'].value_counts()
        axes[0, 0].pie(major_counts, labels=major_counts.index, autopct='%1.1f%%', startangle=90)
        axes[0, 0].set_title('Major Distribution')
        axes[0, 0].axis('equal')  # 确保饼图是圆的
        
        # 2. 性别分布 - 柱状图
        gender_counts = self.students_df['Gender'].value_counts()
        gender_counts.plot(kind='bar', ax=axes[0, 1], color=['#1f77b4', '#ff7f0e'])
        axes[0, 1].set_title('Gender Distribution')
        axes[0, 1].set_xlabel('Gender')
        axes[0, 1].set_ylabel('Number of Students')
        axes[0, 1].set_xticklabels(gender_counts.index, rotation=0)
        
        # 3. GPA分布 - 直方图
        axes[1, 0].hist(self.students_df['GPA'], bins=20, alpha=0.7, color='#2ca02c', edgecolor='black')
        axes[1, 0].set_title('GPA Distribution')
        axes[1, 0].set_xlabel('GPA')
        axes[1, 0].set_ylabel('Frequency')
        
        # 4. 不同专业的GPA分布 - 箱线图
        sns.boxplot(x='Major', y='GPA', data=self.students_df, ax=axes[1, 1])
        axes[1, 1].set_title('GPA Distribution by Major')
        axes[1, 1].set_xlabel('Major')
        axes[1, 1].set_ylabel('GPA')
        
        plt.tight_layout()
        plt.savefig('f:\\课程\\Data Engineering\\assignment1\\output\\attribute_distributions.png')
        plt.close()
        print("Attribute distribution charts saved.")
    
    def visualize_relationships(self):
        """
        可视化属性之间的关系
        """
        if self.students_df is None:
            self.generate_student_data()
        
        # 创建编码后的DataFrame用于相关性分析
        encoded_df = self.students_df.copy()
        label_encoder = LabelEncoder()
        encoded_df['Major_encoded'] = label_encoder.fit_transform(encoded_df['Major'])
        encoded_df['Gender_encoded'] = label_encoder.fit_transform(encoded_df['Gender'])
        
        # 计算相关性矩阵
        corr_matrix = encoded_df[['Major_encoded', 'Gender_encoded', 'GPA']].corr()
        
        # 创建相关性热力图
        plt.figure(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Attribute Correlation Heatmap')
        plt.savefig('f:\\课程\\Data Engineering\\assignment1\\output\\attribute_correlations.png')
        plt.close()
        
        # 创建GPA按性别和专业分组的条形图
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Major', y='GPA', hue='Gender', data=self.students_df)
        plt.title('Average GPA by Major and Gender')
        plt.xlabel('Major')
        plt.ylabel('Average GPA')
        plt.legend(title='Gender')
        plt.savefig('f:\\课程\\Data Engineering\\assignment1\\output\\gpa_by_major_gender.png')
        plt.close()
        
        print("Relationship visualization charts saved.")
    
    def visualize_students_per_major(self):
        """
        计算每个专业的学生数量并使用柱状图显示
        """
        if self.students_df is None:
            self.generate_student_data()
        
        # 计算每个专业的学生数量
        students_per_major = self.students_df['Major'].value_counts()
        
        # 创建柱状图
        plt.figure(figsize=(10, 6))
        bars = plt.bar(students_per_major.index, students_per_major.values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 5, f'{int(height)}',
                     ha='center', va='bottom')
        
        plt.title('Number of Students per Major')
        plt.xlabel('Major')
        plt.ylabel('Number of Students')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig('f:\\课程\\Data Engineering\\assignment1\\output\\students_per_major.png')
        plt.close()
        
        print("Students per major bar chart saved.")
        return students_per_major
    
    def compute_and_visualize_similarity(self):
        """
        随机初始化用户和物品嵌入向量，计算相似度矩阵并使用热力图可视化
        """
        # 随机初始化嵌入向量
        embedding_dim = 8
        self.user_embeddings = np.random.rand(5, embedding_dim)
        self.item_embeddings = np.random.rand(5, embedding_dim)
        
        # 计算相似度矩阵
        # Similarity(U, V) = softmax(U * V^T / sqrt(d))
        dot_product = np.dot(self.user_embeddings, self.item_embeddings.T)
        scaled_dot_product = dot_product / np.sqrt(embedding_dim)
        
        # 应用softmax函数
        exp_scores = np.exp(scaled_dot_product)
        self.similarity_matrix = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        
        # 可视化相似度热力图
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.similarity_matrix, annot=True, cmap='viridis', fmt='.2f')
        plt.title('User-Item Similarity Heatmap')
        plt.xlabel('Item Index')
        plt.ylabel('User Index')
        plt.savefig('f:\\课程\\Data Engineering\\assignment1\\output\\similarity_heatmap.png')
        plt.close()
        
        print("Similarity heatmap saved.")
        return self.similarity_matrix

# 主函数
def main():
    print("Starting Q4 data visualization tasks...")
    
    # 创建可视化器实例
    visualizer = StudentDataVisualizer()
    
    # 生成学生数据
    print("\nPart (b): Generating data for 500 students and visualizing...")
    visualizer.generate_student_data()
    
    # 可视化每个属性的分布
    print("\nVisualizing attribute distributions...")
    visualizer.visualize_attribute_distributions()
    
    # 可视化属性之间的关系
    print("\nVisualizing attribute relationships...")
    visualizer.visualize_relationships()
    
    # Part (c): 计算并可视化每个专业的学生数量
    print("\nPart (c): Calculating number of students per major...")
    students_per_major = visualizer.visualize_students_per_major()
    print("Number of students per major:")
    for major, count in students_per_major.items():
        print(f"{major}: {count} students")
    
    # Part (d): 计算并可视化用户-物品相似度
    print("\nPart (d): Calculating and visualizing user-item similarity...")
    visualizer.compute_and_visualize_similarity()
    
    print("\nQ4 tasks completed! All visualization charts have been saved to the output directory.")

if __name__ == "__main__":
    main()