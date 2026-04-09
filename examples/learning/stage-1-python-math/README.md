# 阶段 1：Python 与数学基础 - 配套代码

## 环境准备

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install numpy pandas matplotlib seaborn jupyter scikit-learn scipy fastapi uvicorn
```

## 文件说明

| 文件 | 内容 | 运行方式 |
|-----|------|---------|
| `scripts/01_python_basics.py` | Python 语法回顾（对比 JS/TS） | `python scripts/01_python_basics.py` |
| `scripts/02_numpy_pandas.py` | NumPy 和 Pandas 核心操作 | `python scripts/02_numpy_pandas.py` |
| `scripts/03_math_concepts.py` | 线性代数、微积分、概率统计 | `python scripts/03_math_concepts.py` |
| `scripts/04_ml_intro.py` | 机器学习入门：线性回归 | `python scripts/04_ml_intro.py` |
| `scripts/05_api_demo.py` | 数据分析 FastAPI 服务 | `uvicorn scripts.05_api_demo:app --reload` |

## 学习建议

1. 按顺序运行每个脚本
2. 修改代码中的参数观察变化
3. 在每个文件底部添加自己的练习
4. 完成后在 `outputs/` 目录写下总结
