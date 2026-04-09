# 阶段 2：经典机器学习 - 配套代码

## 环境准备

```bash
pip install numpy pandas scikit-learn matplotlib seaborn fastapi uvicorn pydantic
```

## 文件说明

| 文件 | 内容 | 运行方式 |
|-----|------|---------|
| `src/01_data_exploration.py` | Titanic 数据探索与清洗 | `python src/01_data_exploration.py` |
| `src/02_model_comparison.py` | 多模型训练与对比 | `python src/02_model_comparison.py` |

## 项目：Titanic 生存预测

完整的从数据到 API 的建模流程：
1. 数据探索 → 2. 多模型对比 → 3. Pipeline + 调参 → 4. 模型解释 → 5. API 封装
