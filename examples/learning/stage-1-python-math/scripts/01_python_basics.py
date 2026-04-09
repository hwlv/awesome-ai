"""
阶段 1 - 脚本 1：Python 语法回顾
面向有 JavaScript/TypeScript 经验的 Web 开发者
"""

# ============================================================
# 1. 列表推导式（替代 JS 的 map/filter）
# ============================================================
print("=" * 50)
print("1. 列表推导式")
print("=" * 50)

# JS: [1,2,3,4,5].filter(x => x > 2).map(x => x * 2)
numbers = [1, 2, 3, 4, 5]
result = [x * 2 for x in numbers if x > 2]
print(f"过滤并映射: {result}")  # [6, 8, 10]

# 嵌套推导式
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(f"乘法表: {matrix}")

# 字典推导式
scores = {"math": 8, "code": 9, "english": 7}
scaled = {k: v * 10 for k, v in scores.items()}
print(f"分数缩放: {scaled}")

# ============================================================
# 2. 生成器（类似 JS 的 Generator，但在 AI 领域更常用）
# ============================================================
print("\n" + "=" * 50)
print("2. 生成器")
print("=" * 50)

def fibonacci(n):
    """斐波那契数列生成器"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

fib_list = list(fibonacci(10))
print(f"斐波那契前10项: {fib_list}")

# 生成器表达式（类似列表推导式，但惰性求值）
squares_gen = (x**2 for x in range(10))
print(f"平方数: {list(squares_gen)}")

# ============================================================
# 3. 装饰器（类似 TS 的 Decorator）
# ============================================================
print("\n" + "=" * 50)
print("3. 装饰器")
print("=" * 50)

import time
from functools import wraps

def timer(func):
    """计时装饰器 —— 在 AI 训练中经常用"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  ⏱️  {func.__name__} 耗时: {elapsed:.4f}s")
        return result
    return wrapper

def retry(max_attempts=3):
    """重试装饰器 —— API 调用常用"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"  ⚠️  第 {attempt} 次失败: {e}，重试中...")
                    time.sleep(0.1)
        return wrapper
    return decorator

@timer
def simulate_training(epochs):
    """模拟训练过程"""
    total = sum(range(epochs * 10000))
    return {"epochs": epochs, "result": total}

result = simulate_training(100)
print(f"训练结果: {result}")

# ============================================================
# 4. 类型标注（和 TypeScript 对比）
# ============================================================
print("\n" + "=" * 50)
print("4. 类型标注")
print("=" * 50)

from typing import List, Dict, Optional, Tuple, Union
from dataclasses import dataclass

# TypeScript 风格的类型定义
# interface User { name: string; age: number; }
@dataclass
class User:
    name: str
    age: int
    role: str = "developer"

# TypeScript: function process(data: Record<string, number>[]): [number[], Stats]
def preprocess(
    data: List[Dict[str, float]],
    normalize: bool = True
) -> Tuple[List[float], Dict[str, float]]:
    """带类型标注的数据预处理函数"""
    values = [d.get("value", 0) for d in data]
    stats = {
        "mean": sum(values) / len(values),
        "max": max(values),
        "min": min(values)
    }
    if normalize:
        mean = stats["mean"]
        values = [v - mean for v in values]
    return values, stats

data = [{"value": 10.0}, {"value": 20.0}, {"value": 30.0}]
values, stats = preprocess(data)
print(f"标准化后的值: {values}")
print(f"统计信息: {stats}")

# ============================================================
# 5. 异常处理
# ============================================================
print("\n" + "=" * 50)
print("5. 异常处理")
print("=" * 50)

class ModelLoadError(Exception):
    """自定义异常 —— AI 应用中建议细分异常类型"""
    pass

def load_model(path: str) -> dict:
    if not path.endswith(".pth"):
        raise ModelLoadError(f"不支持的模型格式: {path}")
    # 模拟加载
    return {"model": "loaded", "path": path}

# try/except/else/finally
for path in ["model.pth", "model.h5", "model.pkl"]:
    try:
        model = load_model(path)
    except ModelLoadError as e:
        print(f"  ❌ 模型加载失败: {e}")
    except Exception as e:
        print(f"  ❌ 未知错误: {e}")
    else:
        print(f"  ✅ 模型加载成功: {model}")
    finally:
        pass  # 清理资源

# ============================================================
# 6. 上下文管理器（类似 JS 的 using 提案）
# ============================================================
print("\n" + "=" * 50)
print("6. 上下文管理器")
print("=" * 50)

from contextlib import contextmanager

@contextmanager
def training_mode(model_name: str):
    """训练模式上下文管理器"""
    print(f"  🚀 开始训练: {model_name}")
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"  ✅ 训练完成: {model_name} ({elapsed:.2f}s)")

with training_mode("ResNet-50"):
    time.sleep(0.1)  # 模拟训练
    print("  📊 训练中...")

print("\n✅ Python 语法回顾完成！")
