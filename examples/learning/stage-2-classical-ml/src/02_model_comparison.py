"""
阶段 2 - 脚本 2：多模型训练与对比
在同一数据集上对比多个算法的表现
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
import warnings
warnings.filterwarnings("ignore")

# ============================================================
# 1. 数据准备
# ============================================================
print("=" * 60)
print("1. 数据准备")
print("=" * 60)

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

try:
    df = pd.read_csv(url)
except Exception:
    # 使用模拟数据
    np.random.seed(42)
    n = 891
    df = pd.DataFrame({
        "Survived": np.random.choice([0, 1], n, p=[0.62, 0.38]),
        "Pclass": np.random.choice([1, 2, 3], n, p=[0.24, 0.21, 0.55]),
        "Sex": np.random.choice(["male", "female"], n, p=[0.65, 0.35]),
        "Age": np.where(np.random.random(n) > 0.2,
                        np.random.normal(30, 14, n).clip(0.5, 80), np.nan),
        "SibSp": np.random.choice(range(6), n, p=[0.68, 0.23, 0.05, 0.02, 0.01, 0.01]),
        "Parch": np.random.choice(range(4), n, p=[0.76, 0.13, 0.09, 0.02]),
        "Fare": np.random.exponential(32, n).clip(0, 512),
        "Embarked": np.random.choice(["S", "C", "Q"], n, p=[0.72, 0.19, 0.09])
    })

# 定义特征
numeric_features = ["Age", "Fare", "SibSp", "Parch"]
categorical_features = ["Pclass", "Sex", "Embarked"]

X = df[numeric_features + categorical_features]
y = df["Survived"]

print(f"数据量: {len(X)}")
print(f"特征数: {len(X.columns)}")
print(f"正负样本比: {y.value_counts().to_dict()}")

# ============================================================
# 2. 构建 Pipeline
# ============================================================
print("\n" + "=" * 60)
print("2. 构建预处理 Pipeline")
print("=" * 60)

# 数值特征：填充 + 标准化
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# 分类特征：填充 + 独热编码
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

print("Pipeline 结构:")
print("  数值特征 → 中位数填充 → 标准化")
print("  分类特征 → 众数填充 → 独热编码")

# ============================================================
# 3. 多模型对比
# ============================================================
print("\n" + "=" * 60)
print("3. 多模型对比（5折交叉验证）")
print("=" * 60)

models = {
    "逻辑回归": LogisticRegression(max_iter=1000, random_state=42),
    "决策树": DecisionTreeClassifier(max_depth=5, random_state=42),
    "随机森林": RandomForestClassifier(n_estimators=100, random_state=42),
    "梯度提升": GradientBoostingClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(kernel="rbf", random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

results = []
print(f"\n{'模型':>8} | {'平均 F1':>8} | {'标准差':>6} | {'得分区间'}")
print("-" * 55)

for name, model in models.items():
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])

    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="f1")
    mean_score = cv_scores.mean()
    std_score = cv_scores.std()

    results.append({
        "模型": name,
        "平均F1": mean_score,
        "标准差": std_score,
        "得分": cv_scores
    })

    print(f"{name:>8} | {mean_score:>8.4f} | {std_score:>6.4f} | "
          f"[{cv_scores.min():.4f} - {cv_scores.max():.4f}]")

# 排序
results.sort(key=lambda x: x["平均F1"], reverse=True)
print(f"\n🏆 最优模型: {results[0]['模型']} (F1={results[0]['平均F1']:.4f})")

# ============================================================
# 4. 最优模型详细评估
# ============================================================
print("\n" + "=" * 60)
print("4. 最优模型详细评估")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

best_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])
best_pipeline.fit(X_train, y_train)
y_pred = best_pipeline.predict(X_test)

print(classification_report(y_test, y_pred, target_names=["未生存", "生存"]))

# ============================================================
# 5. 特征重要性
# ============================================================
print("=" * 60)
print("5. 特征重要性")
print("=" * 60)

# 获取特征名
cat_features_encoded = list(
    best_pipeline.named_steps["preprocessor"]
    .named_transformers_["cat"]
    .named_steps["onehot"]
    .get_feature_names_out(categorical_features)
)
all_features = numeric_features + cat_features_encoded

importances = best_pipeline.named_steps["classifier"].feature_importances_
feature_imp = sorted(
    zip(all_features, importances),
    key=lambda x: x[1], reverse=True
)

print(f"\n{'特征':>20} | {'重要性':>8} | 可视化")
print("-" * 60)
for feat, imp in feature_imp:
    bar = "█" * int(imp * 50)
    print(f"{feat:>20} | {imp:>8.4f} | {bar}")

print("\n✅ 模型对比完成！")
print("\n📝 下一步:")
print("  1. 用 GridSearchCV 调参")
print("  2. 添加特征交叉（如 Age × Pclass）")
print("  3. 将最优模型封装为 API")
