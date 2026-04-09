# 阶段 2：经典机器学习

这一阶段的重点是把"会跑模型"推进到"会做完整建模流程"。

## 阶段目标

- 熟悉数据获取、清洗、特征工程、建模、评估和迭代的完整链路
- 理解常见算法的适用场景和优缺点
- 学会用 scikit-learn Pipeline 组织可复用流程
- 能把最优模型封装成 API

## 算法速查表

| 算法 | 类型 | 适用场景 | 优点 | 缺点 |
|-----|------|---------|------|------|
| 线性回归 | 回归 | 连续值预测 | 简单、可解释 | 只能拟合线性关系 |
| 逻辑回归 | 分类 | 二分类/多分类 | 概率输出、快速 | 线性决策边界 |
| 决策树 | 通用 | 分类和回归 | 可解释性强 | 容易过拟合 |
| 随机森林 | 通用 | 结构化数据 | 稳定、不易过拟合 | 训练较慢 |
| XGBoost | 通用 | 竞赛和生产 | 表现优秀 | 需要调参 |
| KNN | 分类 | 小数据集 | 简单直观 | 高维灾难 |
| SVM | 分类 | 高维数据 | 核技巧强大 | 大数据慢 |

## 核心任务

### 任务 1：数据处理全流程

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# ============================
# 加载和探索数据
# ============================
# 使用经典的 Titanic 数据集
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

print(f"数据形状: {df.shape}")
print(f"\n数据概览:\n{df.head()}")
print(f"\n缺失值统计:\n{df.isnull().sum()}")
print(f"\n数据类型:\n{df.dtypes}")

# ============================
# 数据清洗
# ============================
# 1. 处理缺失值
df["Age"].fillna(df["Age"].median(), inplace=True)
df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)
df.drop("Cabin", axis=1, inplace=True)  # 缺失太多，直接删除

# 2. 特征编码
df["Sex"] = LabelEncoder().fit_transform(df["Sex"])  # male=1, female=0
df = pd.get_dummies(df, columns=["Embarked"], drop_first=True)

# 3. 特征选择
features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare",
            "Embarked_Q", "Embarked_S"]
X = df[features]
y = df["Survived"]

# 4. 数据分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. 特征缩放
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 注意：只用 transform，不用 fit

print(f"\n训练集: {X_train.shape}, 测试集: {X_test.shape}")
print(f"正负样本比: {y_train.value_counts().to_dict()}")
```

### 任务 2：多模型训练与比较

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix
)
import warnings
warnings.filterwarnings("ignore")

# ============================
# 定义多个模型
# ============================
models = {
    "逻辑回归": LogisticRegression(max_iter=1000, random_state=42),
    "决策树": DecisionTreeClassifier(max_depth=5, random_state=42),
    "随机森林": RandomForestClassifier(n_estimators=100, random_state=42),
    "梯度提升": GradientBoostingClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(kernel="rbf", random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

# ============================
# 训练并比较
# ============================
results = []
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    result = {
        "模型": name,
        "准确率": accuracy_score(y_test, y_pred),
        "精确率": precision_score(y_test, y_pred),
        "召回率": recall_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred)
    }
    results.append(result)
    print(f"\n{'='*40}")
    print(f"模型: {name}")
    print(f"{'='*40}")
    print(classification_report(y_test, y_pred))

# 结果对比表
results_df = pd.DataFrame(results).sort_values("F1", ascending=False)
print("\n模型对比排行:")
print(results_df.to_string(index=False))
```

### 任务 3：Pipeline 与交叉验证

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score, GridSearchCV

# ============================
# 构建可复用的 Pipeline
# ============================

# 数值特征处理器
numeric_features = ["Age", "Fare", "SibSp", "Parch"]
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# 分类特征处理器
categorical_features = ["Pclass", "Sex", "Embarked"]
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore"))
])

# 组合预处理器
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# 完整 Pipeline
full_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(random_state=42))
])

# ============================
# 交叉验证
# ============================
# 用原始数据（未手动处理过的）
df_raw = pd.read_csv(url)
X_raw = df_raw[numeric_features + categorical_features]
y_raw = df_raw["Survived"]

cv_scores = cross_val_score(full_pipeline, X_raw, y_raw, cv=5, scoring="f1")
print(f"5折交叉验证 F1 分数: {cv_scores}")
print(f"平均 F1: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")

# ============================
# 超参数网格搜索
# ============================
param_grid = {
    "classifier__n_estimators": [50, 100, 200],
    "classifier__max_depth": [3, 5, 10, None],
    "classifier__min_samples_split": [2, 5, 10]
}

grid_search = GridSearchCV(
    full_pipeline, param_grid, cv=5,
    scoring="f1", n_jobs=-1, verbose=1
)
grid_search.fit(X_raw, y_raw)

print(f"\n最优参数: {grid_search.best_params_}")
print(f"最优 F1: {grid_search.best_score_:.4f}")
```

### 任务 4：模型解释

```python
import numpy as np

# ============================
# 特征重要性
# ============================
best_model = grid_search.best_estimator_

# 获取特征名
feature_names = (
    numeric_features +
    list(best_model.named_steps["preprocessor"]
         .named_transformers_["cat"]
         .named_steps["onehot"]
         .get_feature_names_out(categorical_features))
)

importances = best_model.named_steps["classifier"].feature_importances_
feature_importance = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values("importance", ascending=False)

print("特征重要性排名:")
for _, row in feature_importance.iterrows():
    bar = "█" * int(row["importance"] * 50)
    print(f"  {row['feature']:20s} {row['importance']:.4f} {bar}")

# ============================
# SHAP 解释（可选，需要 pip install shap）
# ============================
# import shap
#
# explainer = shap.TreeExplainer(best_model.named_steps["classifier"])
# X_transformed = best_model.named_steps["preprocessor"].transform(X_raw)
# shap_values = explainer.shap_values(X_transformed)
#
# shap.summary_plot(shap_values[1], X_transformed,
#                   feature_names=feature_names)
```

### 任务 5：模型封装 API

```python
# model_api.py
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Titanic 生存预测 API",
    description="基于随机森林的 Titanic 乘客生存预测服务"
)

# ============================
# 数据模型定义
# ============================
class PassengerInput(BaseModel):
    """乘客信息输入"""
    Pclass: int = Field(..., ge=1, le=3, description="船舱等级 1/2/3")
    Sex: str = Field(..., description="性别 male/female")
    Age: float = Field(..., ge=0, le=120, description="年龄")
    SibSp: int = Field(0, ge=0, description="船上兄弟姐妹/配偶数")
    Parch: int = Field(0, ge=0, description="船上父母/子女数")
    Fare: float = Field(..., ge=0, description="船票价格")
    Embarked: str = Field("S", description="登船港口 C/Q/S")

class PredictionOutput(BaseModel):
    """预测输出"""
    survived: bool
    probability: float
    risk_level: str

# ============================
# 加载模型
# ============================
# 在实际使用前需要先保存模型：
# with open("titanic_model.pkl", "wb") as f:
#     pickle.dump(grid_search.best_estimator_, f)

# model = pickle.load(open("titanic_model.pkl", "rb"))

@app.post("/predict", response_model=PredictionOutput)
async def predict_survival(passenger: PassengerInput):
    """预测乘客生存概率"""
    try:
        import pandas as pd
        input_df = pd.DataFrame([passenger.model_dump()])

        # prediction = model.predict(input_df)[0]
        # probability = model.predict_proba(input_df)[0][1]

        # 模拟预测结果（实际使用时替换为上面的真实预测）
        probability = 0.75
        prediction = probability > 0.5

        risk_level = (
            "低风险" if probability > 0.7
            else "中风险" if probability > 0.4
            else "高风险"
        )

        return PredictionOutput(
            survived=bool(prediction),
            probability=round(probability, 4),
            risk_level=risk_level
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok", "model": "RandomForest-Titanic-v1"}

# 运行: uvicorn model_api:app --reload --port 8000
# 文档: http://localhost:8000/docs
# 测试:
# curl -X POST http://localhost:8000/predict \
#   -H "Content-Type: application/json" \
#   -d '{"Pclass":1,"Sex":"female","Age":29,"SibSp":0,"Parch":0,"Fare":100,"Embarked":"S"}'
```

### 任务 6：写技术报告

每个建模项目结束后，需要有一份简短的技术报告：

```markdown
## Titanic 生存预测 - 技术报告

### 问题定义
- 目标：预测 Titanic 乘客是否能生存
- 类型：二分类问题
- 评估指标：F1 分数（因为正负样本不完全均衡）

### 数据概况
- 样本量：891 条训练数据
- 特征数：7 个（4 数值 + 3 分类）
- 缺失情况：Age 缺失 19.8%，Cabin 缺失 77.1%（已删除）

### 模型对比
| 模型 | F1 | 备注 |
|------|-----|------|
| 逻辑回归 | 0.73 | 基线模型 |
| 随机森林 | 0.78 | 最终选定 |
| 梯度提升 | 0.77 | 表现接近 |

### 关键特征
1. Sex（最重要）：女性生存率显著更高
2. Fare：票价越高生存率越高
3. Pclass：一等舱生存率最高

### 上线风险
- 数据来自 1912 年，规律不一定适用于其他场景
- 模型未考虑乘客姓名中的称谓（Mr/Mrs/Miss）
- 缺失值使用中位数填充，可能引入偏差

### 下一步
- 尝试特征交叉（Age × Pclass）
- 添加称谓特征提取
- 部署后监控预测分布是否稳定
```

## 建议交付物

- 一个从数据到模型的完整项目
- 一份模型评估结果和实验记录
- 一个可交互测试的 API Demo
- 一篇阶段总结，说明模型效果和下一阶段准备度

## 推荐资料

| 资料 | 类型 | 说明 |
|-----|------|------|
| 《Hands-On ML》第 2-9 章 | 书 | 经典 ML 全流程 |
| scikit-learn 官方教程 | 文档 | 最权威的 API 参考 |
| Made With ML | 教程 | 从建模到生产 |
| StatQuest 系列 | 视频 | 算法直觉讲解 |
| Kaggle Learn | 在线课 | 交互式练习 |

## 配套工程建议

这一阶段更适合显式拆出数据、模型和接口：

```text
examples/learning/stage-2-classical-ml/
├─ README.md
├─ data/
│  └─ titanic.csv
├─ src/
│  ├─ 01_data_exploration.py
│  ├─ 02_model_comparison.py
│  ├─ 03_pipeline_cv.py
│  ├─ 04_model_explain.py
│  └─ 05_model_api.py
├─ models/
│  └─ titanic_model.pkl
└─ outputs/
   └─ experiment_log.md
```

目录职责建议：

- `src/`：数据流水线、训练脚本、API 入口
- `models/`：训练输出的模型文件
- `outputs/`：指标、图表、日志

## 常见误区

- 只盯最终指标，不记录特征工程和调参过程
- 模型能跑就算结束，没有解释为什么这个模型更合适
- API 只是包一层壳，没有考虑请求校验和错误处理
- 用测试集来调参（应该只用验证集或交叉验证）
- 不做数据泄漏检查（比如用所有数据的均值来填充缺失值）

## 完成标准

- [ ] 能独立完成一次经典 ML 项目闭环
- [ ] 能解释不同模型在同一任务上的差异
- [ ] 能把训练结果稳定暴露为可消费接口
- [ ] 能说清楚 Pipeline 的好处（可复现、防泄漏）
- [ ] 能写出包含问题定义和风险分析的技术报告
