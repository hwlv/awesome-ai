"""
阶段 3 - 脚本 1：Tensor 与 Autograd 基础
理解 PyTorch 的核心机制
"""

import torch
import numpy as np

# ============================================================
# 1. Tensor 基础
# ============================================================
print("=" * 60)
print("1. Tensor 基础")
print("=" * 60)

print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")

# 检查 Apple Silicon MPS
mps_available = hasattr(torch.backends, 'mps') and torch.backends.mps.is_available()
print(f"MPS 可用 (Apple Silicon): {mps_available}")

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "mps" if mps_available
    else "cpu"
)
print(f"使用设备: {device}\n")

# 创建 Tensor
print("--- 创建 Tensor ---")
x = torch.tensor([1.0, 2.0, 3.0])
print(f"从列表创建: {x}")

matrix = torch.randn(3, 4)
print(f"随机矩阵 (3×4):\n{matrix}")

zeros = torch.zeros(2, 3)
ones = torch.ones(2, 3)
eye = torch.eye(3)
print(f"零矩阵:\n{zeros}")
print(f"单位矩阵:\n{eye}")

# NumPy 互转
print("\n--- NumPy 互转 ---")
np_arr = np.array([1, 2, 3])
tensor = torch.from_numpy(np_arr)
back = tensor.numpy()
print(f"NumPy → Tensor: {tensor}")
print(f"Tensor → NumPy: {back}")

# Tensor 运算
print("\n--- Tensor 运算 ---")
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])
print(f"加法: {a + b}")
print(f"乘法: {a * b}")
print(f"矩阵乘法: {torch.mm(a.unsqueeze(0), b.unsqueeze(1))}")
print(f"点积: {torch.dot(a, b)}")

# 形状操作
print("\n--- 形状操作 ---")
x = torch.randn(2, 3, 4)
print(f"原始形状: {x.shape}")
print(f"reshape: {x.reshape(6, 4).shape}")
print(f"view: {x.view(2, 12).shape}")
print(f"permute: {x.permute(2, 0, 1).shape}")  # 类似 NumPy 的 transpose
print(f"squeeze: {torch.randn(1, 3, 1).squeeze().shape}")
print(f"unsqueeze: {torch.randn(3).unsqueeze(0).shape}")

# ============================================================
# 2. Autograd 自动求导
# ============================================================
print("\n" + "=" * 60)
print("2. Autograd 自动求导")
print("=" * 60)

# 基本求导
print("--- 基本求导 ---")
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x + 1  # y = x² + 2x + 1
y.backward()
print(f"y = x² + 2x + 1")
print(f"x = {x.item()}")
print(f"y = {y.item()}")
print(f"dy/dx = {x.grad.item()} (解析解: 2x + 2 = {2*3+2})")

# 多变量求导
print("\n--- 多变量求导 ---")
w = torch.tensor([2.0, 3.0], requires_grad=True)
x = torch.tensor([1.0, 4.0])
y = w * x
loss = y.sum()
loss.backward()
print(f"w = {w.data}")
print(f"x = {x.data}")
print(f"loss = w·x 的和 = {loss.item()}")
print(f"∂loss/∂w = {w.grad}")  # 应该等于 x

# 链式法则
print("\n--- 链式法则 ---")
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2       # y = x²
z = y ** 3       # z = y³ = x⁶
z.backward()
print(f"z = (x²)³ = x⁶")
print(f"dz/dx = 6x⁵ = {6 * 2**5}")
print(f"PyTorch 计算: {x.grad.item()}")

# ============================================================
# 3. 手写梯度下降
# ============================================================
print("\n" + "=" * 60)
print("3. 手写梯度下降")
print("=" * 60)

# 数据: y = 3x + 2
torch.manual_seed(42)
X = torch.linspace(0, 10, 100)
y_true = 3 * X + 2 + torch.randn(100) * 0.5

# 参数
w = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
lr = 0.01

print(f"目标: y = 3x + 2")
print(f"初始: w = {w.item():.4f}, b = {b.item():.4f}\n")

for epoch in range(200):
    # 前向传播
    y_pred = w * X + b
    loss = ((y_pred - y_true) ** 2).mean()

    # 反向传播
    loss.backward()

    # 更新参数（不追踪梯度）
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad

    # 清零梯度！
    w.grad.zero_()
    b.grad.zero_()

    if epoch % 40 == 0:
        print(f"Epoch {epoch:>3}: w={w.item():.4f}, b={b.item():.4f}, "
              f"loss={loss.item():.4f}")

print(f"\n最终: y = {w.item():.2f}x + {b.item():.2f}")
print(f"目标: y = 3.00x + 2.00")

# ============================================================
# 4. 核心概念总结
# ============================================================
print("\n" + "=" * 60)
print("4. 核心概念总结")
print("=" * 60)

print("""
核心要点:
  1. Tensor 是带自动求导的多维数组
  2. requires_grad=True 开启梯度追踪
  3. loss.backward() 自动计算所有梯度
  4. with torch.no_grad() 在更新参数时关闭追踪
  5. grad.zero_() 必须在每次迭代后清零梯度
  
训练循环的核心模式:
  for epoch in range(epochs):
      y_pred = model(X)          # 前向传播
      loss = criterion(y_pred, y) # 计算损失
      loss.backward()             # 反向传播
      optimizer.step()            # 更新参数
      optimizer.zero_grad()       # 清零梯度
""")

print("✅ Tensor 与 Autograd 基础完成！")
