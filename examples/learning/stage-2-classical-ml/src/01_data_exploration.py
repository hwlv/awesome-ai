"""
阶段 2 - 脚本 1：Titanic 数据探索与清洗
完整的 EDA（探索性数据分析）流程
"""

import pandas as pd
import numpy as np

# ============================================================
# 1. 加载数据
# ============================================================
print("=" * 60)
print("1. 数据加载")
print("=" * 60)

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

try:
    df = pd.read_csv(url)
    print(f"✅ 数据加载成功！")
except Exception as e:
    print(f"❌ 在线数据加载失败: {e}")
    print("创建模拟数据用于演示...")
    np.random.seed(42)
    n = 891
    df = pd.DataFrame({
        "PassengerId": range(1, n + 1),
        "Survived": np.random.choice([0, 1], n, p=[0.62, 0.38]),
        "Pclass": np.random.choice([1, 2, 3], n, p=[0.24, 0.21, 0.55]),
        "Name": [f"Passenger_{i}" for i in range(n)],
        "Sex": np.random.choice(["male", "female"], n, p=[0.65, 0.35]),
        "Age": np.where(np.random.random(n) > 0.2,
                        np.random.normal(30, 14, n).clip(0.5, 80), np.nan),
        "SibSp": np.random.choice(range(6), n, p=[0.68, 0.23, 0.05, 0.02, 0.01, 0.01]),
        "Parch": np.random.choice(range(4), n, p=[0.76, 0.13, 0.09, 0.02]),
        "Ticket": [f"T{np.random.randint(100000, 999999)}" for _ in range(n)],
        "Fare": np.random.exponential(32, n).clip(0, 512),
        "Cabin": np.where(np.random.random(n) > 0.77,
                          [f"{'ABCDEFG'[np.random.randint(7)]}{np.random.randint(1,150)}"
                           for _ in range(n)], np.nan),
        "Embarked": np.random.choice(["S", "C", "Q", np.nan], n, p=[0.70, 0.19, 0.09, 0.02])
    })

print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")

# ============================================================
# 2. 数据概览
# ============================================================
print("\n" + "=" * 60)
print("2. 数据概览")
print("=" * 60)

print(f"\n前 5 行:")
print(df.head())

print(f"\n数据类型:")
print(df.dtypes)

print(f"\n描述性统计:")
print(df.describe())

# ============================================================
# 3. 缺失值分析
# ============================================================
print("\n" + "=" * 60)
print("3. 缺失值分析")
print("=" * 60)

missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(1)
missing_df = pd.DataFrame({
    "缺失数": missing,
    "缺失比例": missing_pct
}).sort_values("缺失数", ascending=False)
missing_df = missing_df[missing_df["缺失数"] > 0]

print(missing_df)
print(f"\n处理策略:")
print(f"  Age: 缺失 {missing_pct.get('Age', 0)}% → 用中位数填充")
print(f"  Cabin: 缺失 {missing_pct.get('Cabin', 0)}% → 删除列")
print(f"  Embarked: 缺失 {missing_pct.get('Embarked', 0)}% → 用众数填充")

# ============================================================
# 4. 特征分析
# ============================================================
print("\n" + "=" * 60)
print("4. 特征分析")
print("=" * 60)

# 生存率分析
print("\n--- 总体生存率 ---")
survival_rate = df["Survived"].mean()
print(f"生存率: {survival_rate:.2%}")

# 按性别
print("\n--- 按性别 ---")
sex_survival = df.groupby("Sex")["Survived"].agg(["mean", "count"])
sex_survival.columns = ["生存率", "人数"]
print(sex_survival)

# 按船舱等级
print("\n--- 按船舱等级 ---")
class_survival = df.groupby("Pclass")["Survived"].agg(["mean", "count"])
class_survival.columns = ["生存率", "人数"]
print(class_survival)

# 按年龄段
print("\n--- 按年龄段 ---")
df["AgeGroup"] = pd.cut(df["Age"], bins=[0, 12, 18, 35, 60, 100],
                         labels=["儿童", "青少年", "青年", "中年", "老年"])
age_survival = df.groupby("AgeGroup")["Survived"].agg(["mean", "count"])
age_survival.columns = ["生存率", "人数"]
print(age_survival)

# ============================================================
# 5. 数据清洗
# ============================================================
print("\n" + "=" * 60)
print("5. 数据清洗")
print("=" * 60)

from sklearn.preprocessing import LabelEncoder

df_clean = df.copy()

# 处理缺失值
df_clean["Age"].fillna(df_clean["Age"].median(), inplace=True)
df_clean["Embarked"].fillna(df_clean["Embarked"].mode()[0], inplace=True)
df_clean.drop("Cabin", axis=1, inplace=True)

# 特征编码
df_clean["Sex"] = LabelEncoder().fit_transform(df_clean["Sex"])
df_clean = pd.get_dummies(df_clean, columns=["Embarked"], drop_first=True)

# 删除不需要的列
df_clean.drop(["PassengerId", "Name", "Ticket", "AgeGroup"], axis=1, inplace=True, errors="ignore")

print(f"清洗后数据形状: {df_clean.shape}")
print(f"缺失值: {df_clean.isnull().sum().sum()}")
print(f"\n清洗后数据:")
print(df_clean.head())

# 保存清洗后的数据
# df_clean.to_csv("data/titanic_cleaned.csv", index=False)
print(f"\n✅ 数据探索和清洗完成！")
