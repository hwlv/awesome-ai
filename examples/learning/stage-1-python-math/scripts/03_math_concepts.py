"""
阶段 1 - 脚本 3：数学概念速查与代码验证
覆盖线性代数、微积分和概率统计核心概念
"""

import numpy as np

# ============================================================
# Part 1: 线性代数
# ============================================================
print("=" * 60)
print("Part 1: 线性代数")
print("=" * 60)

# --- 1.1 向量 ---
print("\n--- 1.1 向量操作 ---")
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"加法: v1 + v2 = {v1 + v2}")
print(f"数乘: 3 * v1 = {3 * v1}")
print(f"点积: v1 · v2 = {np.dot(v1, v2)}")  # 1*4+2*5+3*6=32
print(f"范数(长度): |v1| = {np.linalg.norm(v1):.4f}")

# 余弦相似度 —— AI 中最核心的相似度度量
cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
print(f"余弦相似度: {cos_sim:.4f}")

# --- 1.2 矩阵 ---
print("\n--- 1.2 矩阵操作 ---")
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(f"A =\n{A}")
print(f"B =\n{B}")
print(f"矩阵乘法 A @ B =\n{A @ B}")
print(f"转置 A.T =\n{A.T}")
print(f"行列式 det(A) = {np.linalg.det(A):.2f}")
print(f"逆矩阵 A⁻¹ =\n{np.linalg.inv(A)}")
print(f"验证 A @ A⁻¹ =\n{(A @ np.linalg.inv(A)).round(10)}")

# --- 1.3 特征值和特征向量 ---
print("\n--- 1.3 特征值和特征向量 ---")
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"特征值: {eigenvalues}")
print(f"特征向量:\n{eigenvectors}")
# 验证: A @ v = λ * v
for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]
    lhs = A @ v
    rhs = lam * v
    print(f"验证 λ={lam.real:.4f}: A@v = {lhs.real.round(4)}, λ*v = {rhs.real.round(4)}")

# ============================================================
# Part 2: 微积分
# ============================================================
print("\n" + "=" * 60)
print("Part 2: 微积分")
print("=" * 60)

# --- 2.1 导数 ---
print("\n--- 2.1 数值求导 ---")

def f(x):
    return x ** 2

def numerical_derivative(func, x, h=1e-7):
    """中心差分法求导"""
    return (func(x + h) - func(x - h)) / (2 * h)

for x in [1, 2, 3, 5]:
    deriv = numerical_derivative(f, x)
    print(f"f(x) = x², f'({x}) ≈ {deriv:.6f} (精确值: {2*x})")

# --- 2.2 偏导数和梯度 ---
print("\n--- 2.2 梯度计算 ---")

def loss_function(w):
    """模拟损失函数: L(w1, w2) = w1² + 2*w2²"""
    return w[0]**2 + 2 * w[1]**2

def numerical_gradient(func, w, h=1e-7):
    """数值梯度计算"""
    grad = np.zeros_like(w)
    for i in range(len(w)):
        w_plus = w.copy(); w_plus[i] += h
        w_minus = w.copy(); w_minus[i] -= h
        grad[i] = (func(w_plus) - func(w_minus)) / (2 * h)
    return grad

w = np.array([3.0, 2.0])
grad = numerical_gradient(loss_function, w)
print(f"w = {w}")
print(f"L(w) = {loss_function(w)}")
print(f"∇L(w) = {grad}")
print(f"精确梯度: [2*w1, 4*w2] = [{2*w[0]}, {4*w[1]}]")

# --- 2.3 梯度下降 ---
print("\n--- 2.3 梯度下降演示 ---")

def gradient_descent(func, grad_func, w0, lr=0.1, steps=50):
    """梯度下降优化"""
    w = w0.copy()
    history = []
    for step in range(steps):
        loss = func(w)
        grad = grad_func(func, w)
        history.append({"step": step, "w": w.copy(), "loss": loss, "grad": grad.copy()})
        w = w - lr * grad  # 核心公式：w_new = w_old - lr * gradient
    return w, history

w_init = np.array([4.0, 3.0])
w_final, history = gradient_descent(loss_function, numerical_gradient, w_init, lr=0.1)

print(f"初始点: w = {w_init}, L = {loss_function(w_init)}")
for h in history[::10]:
    print(f"  Step {h['step']:>3}: w = [{h['w'][0]:.4f}, {h['w'][1]:.4f}], L = {h['loss']:.6f}")
print(f"最终点: w = [{w_final[0]:.6f}, {w_final[1]:.6f}], L = {loss_function(w_final):.8f}")

# --- 2.4 常用激活函数 ---
print("\n--- 2.4 激活函数 ---")

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

def tanh(x):
    return np.tanh(x)

x = np.array([-2, -1, 0, 1, 2])
print(f"x       = {x}")
print(f"sigmoid = {sigmoid(x.astype(float)).round(4)}")
print(f"relu    = {relu(x)}")
print(f"tanh    = {tanh(x.astype(float)).round(4)}")

# ============================================================
# Part 3: 概率统计
# ============================================================
print("\n" + "=" * 60)
print("Part 3: 概率统计")
print("=" * 60)

# --- 3.1 基础统计量 ---
print("\n--- 3.1 基础统计量 ---")
np.random.seed(42)
data = np.random.normal(loc=100, scale=15, size=1000)

print(f"均值 (Mean): {np.mean(data):.2f}")
print(f"中位数 (Median): {np.median(data):.2f}")
print(f"方差 (Variance): {np.var(data):.2f}")
print(f"标准差 (Std): {np.std(data):.2f}")
print(f"偏度 (Skewness): {float(np.mean(((data - data.mean()) / data.std()) ** 3)):.4f}")

# --- 3.2 概率分布 ---
print("\n--- 3.2 概率分布 ---")
# 均匀分布
uniform = np.random.uniform(0, 1, 10000)
print(f"均匀分布 [0,1]: 均值={uniform.mean():.4f}, 标准差={uniform.std():.4f}")

# 正态分布
normal = np.random.normal(0, 1, 10000)
print(f"标准正态: 均值={normal.mean():.4f}, 标准差={normal.std():.4f}")

# 伯努利/二项分布
binomial = np.random.binomial(n=10, p=0.5, size=10000)
print(f"二项分布 (n=10, p=0.5): 均值={binomial.mean():.4f} (期望=5)")

# --- 3.3 贝叶斯定理 ---
print("\n--- 3.3 贝叶斯定理 ---")
# 场景：垃圾邮件检测
p_spam = 0.3                     # 先验：30% 是垃圾邮件
p_word_given_spam = 0.8          # 垃圾邮件含"优惠"的概率
p_word_given_ham = 0.1           # 正常邮件含"优惠"的概率

p_word = p_word_given_spam * p_spam + p_word_given_ham * (1 - p_spam)
p_spam_given_word = p_word_given_spam * p_spam / p_word

print(f"P(spam) = {p_spam}")
print(f"P('优惠'|spam) = {p_word_given_spam}")
print(f"P('优惠'|ham) = {p_word_given_ham}")
print(f"P('优惠') = {p_word:.4f}")
print(f"P(spam|'优惠') = {p_spam_given_word:.4f}")
print(f"→ 看到'优惠'后，垃圾邮件概率从 {p_spam:.0%} 上升到 {p_spam_given_word:.0%}")

# --- 3.4 中心极限定理 ---
print("\n--- 3.4 中心极限定理 ---")
print("无论原始分布如何，样本均值的分布趋向正态分布")

# 用均匀分布验证
sample_means = []
for _ in range(10000):
    sample = np.random.uniform(0, 1, 30)  # 从均匀分布取 30 个样本
    sample_means.append(sample.mean())

sample_means = np.array(sample_means)
print(f"原始分布: 均匀分布 [0,1]")
print(f"样本均值的均值: {sample_means.mean():.4f} (理论值: 0.5)")
print(f"样本均值的标准差: {sample_means.std():.4f} (理论值: {1/np.sqrt(12*30):.4f})")

print("\n✅ 数学概念回顾完成！")
print("\n📝 课后练习:")
print("1. 试着用梯度下降求解 f(x) = (x-3)² + 1 的最小值")
print("2. 计算两个文档向量的余弦相似度")
print("3. 用蒙特卡洛方法估算 π 的值")
