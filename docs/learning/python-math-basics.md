# 阶段 1：Python 与数学基础

这一阶段的目标不是"把数学全学完"，而是把后面学机器学习真正会用到的底座补平。

## 阶段目标

- 熟练使用 Python 做基础脚本、数据处理和环境管理
- 掌握 NumPy、Pandas 的常见操作
- 复习线性代数、微积分、概率统计的核心概念
- 理解监督学习、无监督学习、训练集和评估指标这些基础术语

## 核心任务

### 任务 1：搭建 Python 学习环境

```bash
# 安装 Python（推荐 3.10+）
# macOS
brew install python@3.11

# 创建虚拟环境
python3 -m venv ai-study
source ai-study/bin/activate

# 安装基础包
pip install numpy pandas matplotlib seaborn jupyter scikit-learn

# 启动 Jupyter Notebook
jupyter notebook
```

**验收标准：** 能在 Notebook 里运行 `import numpy as np; print(np.__version__)` 并看到输出。

### 任务 2：Python 语法回顾

对于有 JavaScript/TypeScript 经验的开发者，重点关注差异：

```python
# === 1. 列表推导式（替代 JS 的 map/filter）===
# JS: [1,2,3,4,5].filter(x => x > 2).map(x => x * 2)
numbers = [1, 2, 3, 4, 5]
result = [x * 2 for x in numbers if x > 2]  # [6, 8, 10]

# === 2. 字典操作（替代 JS 的 Object）===
user = {"name": "Alice", "age": 30, "role": "developer"}
# 字典推导式
scores = {k: v * 10 for k, v in {"math": 8, "code": 9}.items()}

# === 3. 生成器（类似 JS 的 Generator，但更常用）===
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

list(fibonacci(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# === 4. 装饰器（类似 TS 的 Decorator，但在 AI 领域更常见）===
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.4f}s")
        return result
    return wrapper

@timer
def train_model(epochs):
    """模拟训练过程"""
    time.sleep(0.1 * epochs)
    return {"loss": 0.01}

# === 5. 类型标注（和 TypeScript 对比）===
from typing import List, Dict, Optional, Tuple

def preprocess(
    data: List[Dict[str, float]],
    normalize: bool = True,
    feature_names: Optional[List[str]] = None
) -> Tuple[List[float], Dict[str, float]]:
    """数据预处理函数"""
    pass

# === 6. 异常处理 ===
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"计算错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
finally:
    print("清理资源")
```

### 任务 3：NumPy 与 Pandas 数据处理

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === NumPy 核心操作 ===

# 创建数组
arr = np.array([1, 2, 3, 4, 5])
matrix = np.random.randn(3, 4)  # 3x4 随机矩阵

# 向量化运算 —— 比 Python 循环快 100 倍
a = np.random.randn(1000000)
b = np.random.randn(1000000)
dot_product = np.dot(a, b)  # 向量点积

# 广播机制
matrix = np.random.randn(3, 4)
row_mean = matrix.mean(axis=1, keepdims=True)
normalized = matrix - row_mean  # 每行减去该行均值

# 索引和切片
matrix = np.arange(20).reshape(4, 5)
print(matrix[1:3, 2:4])    # 取第 2-3 行、第 3-4 列
print(matrix[matrix > 10])  # 布尔索引

# === Pandas 核心操作 ===

# 读取数据
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "age": [28, 35, 42, 31],
    "salary": [75000, 92000, 108000, 85000],
    "department": ["Engineering", "Marketing", "Engineering", "Marketing"]
})

# 数据探索（Web 开发者习惯用 console.log，这里用这些）
print(df.shape)         # (4, 4) 行数和列数
print(df.dtypes)        # 每列数据类型
print(df.describe())    # 描述性统计
print(df.info())        # 数据结构信息

# 数据清洗
df_dirty = pd.DataFrame({
    "price": [100, None, 200, 300, None],
    "category": ["A", "B", "A", None, "B"],
    "date": ["2024-01-01", "2024-01-02", "invalid", "2024-01-04", "2024-01-05"]
})

# 处理缺失值
df_dirty["price"].fillna(df_dirty["price"].mean(), inplace=True)
df_dirty["category"].fillna("Unknown", inplace=True)

# 分组聚合（类似 SQL 的 GROUP BY）
dept_stats = df.groupby("department").agg(
    avg_salary=("salary", "mean"),
    count=("name", "count"),
    max_age=("age", "max")
).reset_index()

print(dept_stats)
```

### 任务 4：数学概念速查与代码验证

```python
import numpy as np
import matplotlib.pyplot as plt

# ============================
# 线性代数核心概念
# ============================

# 1. 向量和矩阵
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

# 点积：衡量两个向量的相似度
# 在 AI 里用于：注意力机制、相似度计算
dot = np.dot(v1, v2)  # 1*4 + 2*5 + 3*6 = 32

# 2. 矩阵乘法
# 在 AI 里用于：神经网络的前向传播
W = np.random.randn(3, 4)  # 权重矩阵
x = np.random.randn(4, 1)  # 输入向量
y = W @ x                   # 输出 = 权重 × 输入

# 3. 矩阵转置和逆
A = np.array([[1, 2], [3, 4]])
A_T = A.T          # 转置
A_inv = np.linalg.inv(A)  # 逆矩阵
print(A @ A_inv)   # 应该接近单位矩阵

# ============================
# 微积分核心概念
# ============================

# 1. 导数 = 变化率
# 在 AI 里用于：梯度下降优化
def f(x):
    return x ** 2

def numerical_derivative(func, x, h=1e-7):
    """数值求导"""
    return (func(x + h) - func(x - h)) / (2 * h)

print(f"f(x)=x² 在 x=3 处的导数: {numerical_derivative(f, 3)}")  # ≈ 6

# 2. 梯度 = 多变量函数的导数向量
# 在 AI 里用于：指示参数更新方向
def loss_function(w):
    """模拟损失函数 L(w1, w2) = w1² + 2*w2²"""
    return w[0]**2 + 2 * w[1]**2

def numerical_gradient(func, w, h=1e-7):
    """数值计算梯度"""
    grad = np.zeros_like(w)
    for i in range(len(w)):
        w_plus = w.copy()
        w_minus = w.copy()
        w_plus[i] += h
        w_minus[i] -= h
        grad[i] = (func(w_plus) - func(w_minus)) / (2 * h)
    return grad

w = np.array([3.0, 2.0])
grad = numerical_gradient(loss_function, w)
print(f"梯度: {grad}")  # [6.0, 8.0]

# 3. 梯度下降可视化
def gradient_descent_demo():
    """一个最简单的梯度下降示例"""
    w = np.array([4.0, 4.0])
    lr = 0.1
    history = [w.copy()]

    for step in range(20):
        grad = numerical_gradient(loss_function, w)
        w = w - lr * grad
        history.append(w.copy())
        if step % 5 == 0:
            print(f"Step {step}: w={w}, loss={loss_function(w):.4f}")

    return history

history = gradient_descent_demo()

# ============================
# 概率统计核心概念
# ============================

# 1. 均值、方差和标准差
data = np.random.normal(loc=100, scale=15, size=1000)
print(f"均值: {np.mean(data):.2f}")
print(f"方差: {np.var(data):.2f}")
print(f"标准差: {np.std(data):.2f}")

# 2. 正态分布
from scipy import stats
x = np.linspace(-4, 4, 100)
y = stats.norm.pdf(x, 0, 1)

# 3. 贝叶斯定理的直觉
# P(A|B) = P(B|A) * P(A) / P(B)
# 在 AI 里用于：朴素贝叶斯分类器、概率推断
p_spam = 0.3                    # 先验概率：垃圾邮件比例
p_word_given_spam = 0.8         # 垃圾邮件包含"优惠"的概率
p_word_given_not_spam = 0.1     # 正常邮件包含"优惠"的概率

p_word = p_word_given_spam * p_spam + p_word_given_not_spam * (1 - p_spam)
p_spam_given_word = p_word_given_spam * p_spam / p_word

print(f"看到'优惠'后判断为垃圾邮件的概率: {p_spam_given_word:.2%}")
```

### 任务 5：理解 ML 基础概念

```python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ============================
# 最简单的机器学习：线性回归
# ============================

# 生成模拟数据：房屋面积 → 房价
np.random.seed(42)
area = np.random.uniform(50, 200, 100)  # 面积 50-200 平方米
price = 5000 * area + 100000 + np.random.normal(0, 50000, 100)  # 价格 = 5000*面积 + 噪声

# 转为二维数组（sklearn 要求）
X = area.reshape(-1, 1)
y = price

# ============================
# 关键概念：训练集 / 测试集分割
# ============================
# 为什么要分割？—— 防止"开卷考试"
# 训练集：用于学习参数
# 测试集：用于验证模型在新数据上的表现
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"训练集大小: {len(X_train)}, 测试集大小: {len(X_test)}")

# ============================
# 训练模型
# ============================
model = LinearRegression()
model.fit(X_train, y_train)

print(f"学到的斜率 (每平方米价格): {model.coef_[0]:.0f}")
print(f"学到的截距: {model.intercept_:.0f}")

# ============================
# 评估模型
# ============================
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"均方误差 (MSE): {mse:,.0f}")
print(f"R² 分数: {r2:.4f}")  # 越接近 1 越好

# ============================
# 过拟合 vs 欠拟合 演示
# ============================
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# 生成对比数据
degrees = [1, 4, 15]
for degree in degrees:
    model = make_pipeline(
        PolynomialFeatures(degree),
        LinearRegression()
    )
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"多项式次数={degree}: 训练R²={train_score:.4f}, 测试R²={test_score:.4f}")
    # degree=1  → 简单模型，可能欠拟合
    # degree=4  → 适中，通常最好
    # degree=15 → 复杂模型，可能过拟合（训练好，测试差）
```

## 建议实践

- 做 2 到 3 个 Kaggle 入门题或 Hugging Face 入门实验
- 用公开数据集完成一次小型 EDA（探索性数据分析）
- 写一个简单 API，把数据处理结果返回成 JSON

### 小型 EDA 实践参考

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 用 Seaborn 内置的 Tips 数据集做 EDA
tips = sns.load_dataset("tips")

print("=" * 50)
print("数据概览")
print("=" * 50)
print(f"数据量: {tips.shape[0]} 行, {tips.shape[1]} 列")
print(f"\n列名: {list(tips.columns)}")
print(f"\n数据类型:\n{tips.dtypes}")
print(f"\n前 5 行:\n{tips.head()}")
print(f"\n描述性统计:\n{tips.describe()}")
print(f"\n缺失值:\n{tips.isnull().sum()}")

# 核心分析
print("\n按日期统计平均小费比例:")
tips["tip_ratio"] = tips["tip"] / tips["total_bill"]
daily = tips.groupby("day")["tip_ratio"].mean().sort_values(ascending=False)
print(daily)
```

### 数据处理 API 实践

```python
# api_demo.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI(title="数据分析 API")

class DataSummaryRequest(BaseModel):
    data: list[dict]

class DataSummaryResponse(BaseModel):
    row_count: int
    column_count: int
    columns: list[str]
    numeric_summary: dict

@app.post("/analyze", response_model=DataSummaryResponse)
async def analyze_data(request: DataSummaryRequest):
    """接收 JSON 数据，返回统计摘要"""
    df = pd.DataFrame(request.data)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    summary = {}
    for col in numeric_cols:
        summary[col] = {
            "mean": float(df[col].mean()),
            "std": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max())
        }

    return DataSummaryResponse(
        row_count=len(df),
        column_count=len(df.columns),
        columns=list(df.columns),
        numeric_summary=summary
    )

# 运行: uvicorn api_demo:app --reload
# 测试: curl -X POST http://localhost:8000/analyze \
#   -H "Content-Type: application/json" \
#   -d '{"data": [{"name":"A","score":85},{"name":"B","score":92}]}'
```

## 建议交付物

- 至少 3 个结构清晰的 Notebook 或脚本
- 一份数学概念笔记，覆盖至少 10 个核心概念
- 一篇阶段总结，回答"我现在能独立完成什么"

## 推荐资料

| 资料 | 类型 | 说明 |
|-----|------|------|
| 《Python Crash Course》前 12 章 | 书 | Python 语法入门 |
| Real Python | 网站 | Python 实战教程 |
| Kaggle Learn Python & Pandas | 在线课 | 交互式练习 |
| 3Blue1Brown 线性代数系列 | 视频 | 最好的数学直觉视频 |
| Andrew Ng 机器学习课前几周 | 视频 | ML 基础概念 |
| 《Hands-On ML》第 1 章 | 书 | ML 全景图 |

## 配套工程建议

如果要在当前仓库放这个阶段的代码，建议拆成下面这样：

```text
examples/learning/stage-1-python-math/
├─ README.md
├─ scripts/
│  ├─ 01_python_basics.py
│  ├─ 02_numpy_pandas.py
│  ├─ 03_math_concepts.py
│  ├─ 04_ml_intro.py
│  └─ 05_api_demo.py
├─ notebooks/
│  └─ eda_practice.ipynb
└─ outputs/
```

这样比把说明和任务清单混在代码目录里更容易维护：

- `README.md` 负责介绍怎么运行
- `scripts/` 放一次性演示代码
- `notebooks/` 放探索式实验
- `outputs/` 放图表和导出结果

## 常见误区

- 一开始就去追模型和框架名字，结果基础数据处理能力没跟上
- 只看数学定义，不把公式变成代码和图表
- 做了练习但没有留下结论，后面回头几乎等于重学
- 从 JS 切到 Python 时，不适应缩进和动态类型，花太多时间在语法纠结上

## 完成标准

- [ ] 能独立写一个数据处理脚本并解释输出
- [ ] 能说清楚常见机器学习概念之间的关系
- [ ] 能看懂并改动一个最小的 Python 数据分析项目
- [ ] 能用 NumPy 做矩阵运算、用 Pandas 做数据聚合
- [ ] 能手写梯度下降的核心逻辑
