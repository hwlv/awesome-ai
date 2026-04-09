"""
阶段 1 - 脚本 4：机器学习入门 - 线性回归
理解 ML 的核心概念：训练、评估、过拟合
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score

# ============================================================
# 1. 生成模拟数据
# ============================================================
print("=" * 60)
print("1. 数据准备")
print("=" * 60)

np.random.seed(42)
# 模拟房价数据：price = 5000 * area + noise
area = np.random.uniform(50, 200, 200)
price = 5000 * area + 100000 + np.random.normal(0, 50000, 200)

X = area.reshape(-1, 1)
y = price

print(f"样本数: {len(X)}")
print(f"面积范围: [{area.min():.1f}, {area.max():.1f}] 平方米")
print(f"价格范围: [{price.min():.0f}, {price.max():.0f}] 元")

# ============================================================
# 2. 训练集 / 测试集分割
# ============================================================
print("\n" + "=" * 60)
print("2. 数据分割")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"训练集: {len(X_train)} 样本")
print(f"测试集: {len(X_test)} 样本")
print("为什么要分割？防止模型'背答案'（过拟合）")

# ============================================================
# 3. 训练线性回归
# ============================================================
print("\n" + "=" * 60)
print("3. 训练线性回归模型")
print("=" * 60)

model = LinearRegression()
model.fit(X_train, y_train)

print(f"学到的公式: price = {model.coef_[0]:.0f} × area + {model.intercept_:.0f}")
print(f"（真实公式: price = 5000 × area + 100000）")

# 预测
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n评估结果:")
print(f"  均方误差 (MSE): {mse:,.0f}")
print(f"  均方根误差 (RMSE): {np.sqrt(mse):,.0f}")
print(f"  R² 分数: {r2:.4f} (越接近 1 越好)")

# ============================================================
# 4. 过拟合 vs 欠拟合
# ============================================================
print("\n" + "=" * 60)
print("4. 过拟合 vs 欠拟合演示")
print("=" * 60)

degrees = [1, 3, 5, 10, 15]
print(f"\n{'多项式次数':>8} | {'训练 R²':>8} | {'测试 R²':>8} | {'状态':>6}")
print("-" * 45)

for degree in degrees:
    pipe = make_pipeline(
        PolynomialFeatures(degree),
        LinearRegression()
    )
    pipe.fit(X_train, y_train)
    train_r2 = pipe.score(X_train, y_train)
    test_r2 = pipe.score(X_test, y_test)

    if test_r2 < 0.7:
        status = "欠拟合"
    elif train_r2 - test_r2 > 0.1:
        status = "过拟合"
    else:
        status = "✅ 合适"

    print(f"{degree:>8} | {train_r2:>8.4f} | {test_r2:>8.4f} | {status}")

print("\n关键概念:")
print("  欠拟合：模型太简单，训练和测试都不好")
print("  过拟合：模型太复杂，训练好但测试差（'背答案'）")
print("  合适：训练和测试都不错，泛化能力好")

# ============================================================
# 5. 预测示例
# ============================================================
print("\n" + "=" * 60)
print("5. 使用模型预测")
print("=" * 60)

test_areas = [60, 80, 100, 120, 150, 180]
for a in test_areas:
    pred = model.predict([[a]])[0]
    actual = 5000 * a + 100000
    diff = abs(pred - actual)
    print(f"  面积 {a:>3} m² → 预测: ¥{pred:>10,.0f} | 真实: ¥{actual:>10,.0f} | 误差: ¥{diff:>8,.0f}")

print("\n✅ 机器学习入门完成！")
print("\n📝 核心要点:")
print("  1. ML = 从数据中学习规律（参数）")
print("  2. 训练集用来学习，测试集用来验证")
print("  3. 模型太简单会欠拟合，太复杂会过拟合")
print("  4. 选择合适的模型复杂度是关键")
