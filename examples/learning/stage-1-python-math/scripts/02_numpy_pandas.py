"""
阶段 1 - 脚本 2：NumPy 与 Pandas 核心操作
这两个库是 AI/ML 的基座，必须熟练掌握
"""

import numpy as np
import pandas as pd

# ============================================================
# Part 1: NumPy 核心操作
# ============================================================
print("=" * 60)
print("Part 1: NumPy 核心操作")
print("=" * 60)

# --- 1.1 创建数组 ---
print("\n--- 1.1 创建数组 ---")
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
random_arr = np.random.randn(3, 4)  # 标准正态分布
arange = np.arange(0, 10, 2)       # 类似 range
linspace = np.linspace(0, 1, 5)    # 均匀分布的点

print(f"一维数组: {arr}")
print(f"矩阵形状: {matrix.shape}")
print(f"等差数列: {arange}")
print(f"均匀分布: {linspace}")

# --- 1.2 向量化运算 ---
print("\n--- 1.2 向量化运算 ---")
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(f"加法: {a + b}")
print(f"乘法: {a * b}")        # 逐元素乘法
print(f"点积: {np.dot(a, b)}")  # 1*4 + 2*5 + 3*6 = 32
print(f"幂运算: {a ** 2}")

# 性能对比
import time
size = 1_000_000
data = np.random.randn(size)

start = time.time()
result_loop = [x ** 2 for x in data]
loop_time = time.time() - start

start = time.time()
result_numpy = data ** 2
numpy_time = time.time() - start

print(f"\nPython 循环: {loop_time:.4f}s")
print(f"NumPy 向量化: {numpy_time:.4f}s")
print(f"加速比: {loop_time / numpy_time:.0f}x")

# --- 1.3 广播机制 ---
print("\n--- 1.3 广播机制 ---")
matrix = np.random.randn(3, 4)
row_mean = matrix.mean(axis=1, keepdims=True)
centered = matrix - row_mean  # 每行减去行均值
print(f"矩阵形状: {matrix.shape}")
print(f"行均值形状: {row_mean.shape}")
print(f"中心化后行均值: {centered.mean(axis=1).round(10)}")  # 应该接近 0

# --- 1.4 索引和切片 ---
print("\n--- 1.4 索引和切片 ---")
m = np.arange(20).reshape(4, 5)
print(f"原矩阵:\n{m}")
print(f"第 2 行: {m[1]}")
print(f"第 2-3 行，第 3-4 列:\n{m[1:3, 2:4]}")
print(f"大于 10 的元素: {m[m > 10]}")
print(f"偶数元素: {m[m % 2 == 0]}")

# --- 1.5 常用统计函数 ---
print("\n--- 1.5 常用统计函数 ---")
data = np.random.randn(1000)
print(f"均值: {data.mean():.4f}")
print(f"标准差: {data.std():.4f}")
print(f"最大值: {data.max():.4f}")
print(f"最小值: {data.min():.4f}")
print(f"中位数: {np.median(data):.4f}")
print(f"25 分位数: {np.percentile(data, 25):.4f}")
print(f"75 分位数: {np.percentile(data, 75):.4f}")

# ============================================================
# Part 2: Pandas 核心操作
# ============================================================
print("\n" + "=" * 60)
print("Part 2: Pandas 核心操作")
print("=" * 60)

# --- 2.1 创建 DataFrame ---
print("\n--- 2.1 创建 DataFrame ---")
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age": [28, 35, 42, 31, 27],
    "salary": [75000, 92000, 108000, 85000, 71000],
    "department": ["Engineering", "Marketing", "Engineering", "Marketing", "Engineering"],
    "years": [3, 7, 12, 5, 2]
})
print(df)
print(f"\n形状: {df.shape}")
print(f"列名: {list(df.columns)}")

# --- 2.2 数据探索 ---
print("\n--- 2.2 数据探索 ---")
print(f"数据类型:\n{df.dtypes}\n")
print(f"描述性统计:\n{df.describe()}\n")
print(f"唯一值: department = {df['department'].unique()}")
print(f"值计数:\n{df['department'].value_counts()}")

# --- 2.3 数据清洗 ---
print("\n--- 2.3 数据清洗 ---")
dirty = pd.DataFrame({
    "price": [100, None, 200, 300, None, 400],
    "category": ["A", "B", "A", None, "B", "C"],
    "date": ["2024-01-01", "2024-01-02", "invalid", "2024-01-04", None, "2024-01-06"]
})
print(f"原始数据:\n{dirty}\n")
print(f"缺失值:\n{dirty.isnull().sum()}\n")

# 填充缺失值
cleaned = dirty.copy()
cleaned["price"].fillna(cleaned["price"].mean(), inplace=True)
cleaned["category"].fillna("Unknown", inplace=True)
cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
print(f"清洗后:\n{cleaned}")

# --- 2.4 数据筛选和变换 ---
print("\n--- 2.4 数据筛选和变换 ---")
# 条件筛选
senior = df[df["years"] >= 5]
print(f"5年以上员工:\n{senior}\n")

# 多条件
eng_senior = df[(df["department"] == "Engineering") & (df["salary"] > 75000)]
print(f"工程部高薪员工:\n{eng_senior}\n")

# 新增列
df["salary_rank"] = df["salary"].rank(ascending=False).astype(int)
df["is_senior"] = df["years"] >= 5
print(f"添加计算列后:\n{df}")

# --- 2.5 分组聚合 ---
print("\n--- 2.5 分组聚合 ---")
dept_stats = df.groupby("department").agg(
    avg_salary=("salary", "mean"),
    max_salary=("salary", "max"),
    count=("name", "count"),
    avg_years=("years", "mean")
).reset_index()
print(f"部门统计:\n{dept_stats}")

# --- 2.6 排序和排名 ---
print("\n--- 2.6 排序和排名 ---")
sorted_df = df.sort_values("salary", ascending=False)
print(f"薪资排名:\n{sorted_df[['name', 'salary', 'salary_rank']]}")

# --- 2.7 数据合并 ---
print("\n--- 2.7 数据合并 ---")
projects = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Frank"],
    "project": ["AI Chat", "Campaign", "Infrastructure", "Design"]
})
merged = pd.merge(df, projects, on="name", how="left")
print(f"合并后:\n{merged[['name', 'department', 'project']]}")

print("\n✅ NumPy 与 Pandas 练习完成！")
