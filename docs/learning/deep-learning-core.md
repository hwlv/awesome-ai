# 阶段 3：深度学习核心

这一阶段的重点是理解训练循环和模型结构，不是追求"把所有深度学习方向都学一遍"。

## 阶段目标

- 掌握 PyTorch 基础：Tensor、Autograd、Module、Dataset、DataLoader
- 能独立写出训练、验证和保存模型的流程
- 实现一个图像或文本分类任务
- 把模型部署成服务并观察基本性能

## 深度学习核心概念速查

| 概念 | 解释 | 类比 |
|-----|------|------|
| Tensor | 多维数组，支持 GPU 加速 | 类似 NumPy 的 ndarray |
| Autograd | 自动计算梯度 | 类似 JS 的响应式数据追踪 |
| Module | 神经网络层的基类 | 类似 React 的 Component |
| Loss Function | 衡量预测和真实值的差距 | 类似单元测试的断言 |
| Optimizer | 根据梯度更新参数 | 类似编译器的优化器 |
| DataLoader | 批量加载数据 | 类似 Node.js 的 Stream |
| Epoch | 遍历完整数据集一次 | 类似一轮 CI/CD 流水线 |

## 核心任务

### 任务 1：PyTorch 基础 - Tensor 与 Autograd

```python
import torch
import numpy as np

# ============================
# Tensor 基础
# ============================
print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")
print(f"MPS 可用: {torch.backends.mps.is_available()}")  # Apple Silicon

# 创建 Tensor
x = torch.tensor([1.0, 2.0, 3.0])
matrix = torch.randn(3, 4)
zeros = torch.zeros(2, 3)
ones = torch.ones(2, 3)

# 从 NumPy 转换（Web 开发者可以理解为 JSON.parse/stringify）
np_array = np.array([1, 2, 3])
tensor_from_np = torch.from_numpy(np_array)
back_to_np = tensor_from_np.numpy()

# GPU 加速（如果可用）
device = torch.device("cuda" if torch.cuda.is_available()
                      else "mps" if torch.backends.mps.is_available()
                      else "cpu")
x = x.to(device)
print(f"设备: {device}")

# ============================
# Autograd 自动求导
# ============================
# 这是深度学习最核心的机制之一
# 类似于 JS 的 Proxy，PyTorch 会自动追踪所有运算

# 声明需要计算梯度的张量
w = torch.tensor([2.0, 3.0], requires_grad=True)
x = torch.tensor([1.0, 4.0])

# 前向传播：计算输出
y = w * x       # 逐元素乘法
loss = y.sum()   # 模拟损失函数

# 反向传播：自动计算梯度
loss.backward()

print(f"w = {w.data}")
print(f"x = {x.data}")
print(f"loss = {loss.item()}")
print(f"∂loss/∂w = {w.grad}")  # 梯度 = x = [1.0, 4.0]

# ============================
# 手写梯度下降
# ============================
def manual_gradient_descent():
    """从零实现梯度下降，理解核心循环"""
    # 真实函数: y = 3x + 2
    X = torch.linspace(0, 10, 100)
    y_true = 3 * X + 2 + torch.randn(100) * 0.5

    # 可学习参数
    w = torch.tensor([0.0], requires_grad=True)
    b = torch.tensor([0.0], requires_grad=True)
    lr = 0.01

    for epoch in range(100):
        # 前向传播
        y_pred = w * X + b
        loss = ((y_pred - y_true) ** 2).mean()

        # 反向传播
        loss.backward()

        # 更新参数（不追踪梯度）
        with torch.no_grad():
            w -= lr * w.grad
            b -= lr * b.grad

        # 清零梯度（PyTorch 默认会累加梯度）
        w.grad.zero_()
        b.grad.zero_()

        if epoch % 20 == 0:
            print(f"Epoch {epoch}: w={w.item():.4f}, b={b.item():.4f}, "
                  f"loss={loss.item():.4f}")

    print(f"\n最终结果: y = {w.item():.2f}x + {b.item():.2f}")
    print(f"真实函数: y = 3.00x + 2.00")

manual_gradient_descent()
```

### 任务 2：构建神经网络 - MNIST 手写数字识别

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# ============================
# 1. 数据准备
# ============================
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))  # MNIST 的均值和标准差
])

train_dataset = datasets.MNIST(
    root="./data", train=True, download=True, transform=transform
)
test_dataset = datasets.MNIST(
    root="./data", train=False, download=True, transform=transform
)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

print(f"训练集: {len(train_dataset)} 张图片")
print(f"测试集: {len(test_dataset)} 张图片")
print(f"图片尺寸: {train_dataset[0][0].shape}")  # [1, 28, 28]

# ============================
# 2. 定义网络（类比 React Component）
# ============================
class MNISTNet(nn.Module):
    """
    一个简单的全连接网络
    类比 Web 开发：
    - __init__ 相当于 constructor
    - forward 相当于 render
    - 每一层相当于一个子组件
    """
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.layers = nn.Sequential(
            nn.Linear(28 * 28, 256),    # 输入层：784 → 256
            nn.ReLU(),                   # 激活函数
            nn.Dropout(0.2),             # 正则化，防止过拟合
            nn.Linear(256, 128),         # 隐层：256 → 128
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 10)           # 输出层：128 → 10（0-9 十个类别）
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.layers(x)

# 初始化
device = torch.device("cuda" if torch.cuda.is_available()
                      else "mps" if torch.backends.mps.is_available()
                      else "cpu")
model = MNISTNet().to(device)
print(f"\n模型结构:\n{model}")
print(f"参数总量: {sum(p.numel() for p in model.parameters()):,}")

# ============================
# 3. 定义损失函数和优化器
# ============================
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# ============================
# 4. 训练循环（深度学习的核心模式）
# ============================
def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for batch_idx, (data, target) in enumerate(loader):
        data, target = data.to(device), target.to(device)

        # 前向传播
        output = model(data)
        loss = criterion(output, target)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 统计
        total_loss += loss.item()
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += target.size(0)

    avg_loss = total_loss / len(loader)
    accuracy = correct / total
    return avg_loss, accuracy


def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for data, target in loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            total_loss += criterion(output, target).item()
            pred = output.argmax(dim=1)
            correct += pred.eq(target).sum().item()
            total += target.size(0)

    avg_loss = total_loss / len(loader)
    accuracy = correct / total
    return avg_loss, accuracy


# 训练
EPOCHS = 10
best_accuracy = 0

print("\n开始训练...")
print(f"{'Epoch':>5} | {'Train Loss':>10} | {'Train Acc':>9} | "
      f"{'Test Loss':>9} | {'Test Acc':>8}")
print("-" * 60)

for epoch in range(1, EPOCHS + 1):
    train_loss, train_acc = train_one_epoch(
        model, train_loader, criterion, optimizer, device
    )
    test_loss, test_acc = evaluate(model, test_loader, criterion, device)

    print(f"{epoch:>5} | {train_loss:>10.4f} | {train_acc:>8.2%} | "
          f"{test_loss:>9.4f} | {test_acc:>7.2%}")

    # 保存最优模型
    if test_acc > best_accuracy:
        best_accuracy = test_acc
        torch.save(model.state_dict(), "best_mnist_model.pth")

print(f"\n最优测试准确率: {best_accuracy:.2%}")
```

### 任务 3：CNN 图像分类 - CIFAR-10

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# ============================
# 1. 数据增强和加载
# ============================
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465),
                         (0.2470, 0.2435, 0.2616))
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465),
                         (0.2470, 0.2435, 0.2616))
])

train_dataset = datasets.CIFAR10(
    root="./data", train=True, download=True, transform=train_transform
)
test_dataset = datasets.CIFAR10(
    root="./data", train=False, download=True, transform=test_transform
)

train_loader = DataLoader(train_dataset, batch_size=128,
                          shuffle=True, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=256,
                         shuffle=False, num_workers=2)

CLASSES = ["飞机", "汽车", "鸟", "猫", "鹿",
           "狗", "蛙", "马", "船", "卡车"]

# ============================
# 2. 定义 CNN 模型
# ============================
class CIFAR10Net(nn.Module):
    """
    类比 Web 开发中的中间件栈：
    - Conv2d: 提取局部特征（类似正则匹配）
    - BatchNorm: 标准化（类似数据校验中间件）
    - MaxPool: 降维（类似数据聚合）
    - FC: 最终分类（类似路由分发）
    """
    def __init__(self, num_classes=10):
        super().__init__()

        # 特征提取器
        self.features = nn.Sequential(
            # Block 1: 3 → 32 通道
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),    # 32x32 → 16x16
            nn.Dropout2d(0.25),

            # Block 2: 32 → 64 通道
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),    # 16x16 → 8x8
            nn.Dropout2d(0.25),

            # Block 3: 64 → 128 通道
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),    # 8x8 → 4x4
            nn.Dropout2d(0.25),
        )

        # 分类器
        self.classifier = nn.Sequential(
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)  # Flatten
        x = self.classifier(x)
        return x

model = CIFAR10Net().to(device)
print(f"模型参数量: {sum(p.numel() for p in model.parameters()):,}")

# ============================
# 3. 训练配置
# ============================
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

# ============================
# 4. 训练（带学习率调度和早停）
# ============================
EPOCHS = 50
best_acc = 0
patience = 10
patience_counter = 0

for epoch in range(1, EPOCHS + 1):
    train_loss, train_acc = train_one_epoch(
        model, train_loader, criterion, optimizer, device
    )
    test_loss, test_acc = evaluate(model, test_loader, criterion, device)
    scheduler.step()

    lr = optimizer.param_groups[0]["lr"]
    print(f"Epoch {epoch:>3} | LR: {lr:.6f} | "
          f"Train: {train_acc:.2%} | Test: {test_acc:.2%}")

    if test_acc > best_acc:
        best_acc = test_acc
        patience_counter = 0
        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "best_acc": best_acc
        }, "best_cifar10_model.pth")
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"早停！在 Epoch {epoch}，最优准确率: {best_acc:.2%}")
            break

print(f"\n最优测试准确率: {best_acc:.2%}")
```

### 任务 4：文本分类 - 情感分析

```python
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from collections import Counter

# ============================
# 1. 简单文本数据集
# ============================
# 模拟数据（实际项目中用 IMDB、SST 等数据集）
texts = [
    ("这个产品太好了，非常满意", 1),
    ("质量很差，不推荐购买", 0),
    ("性价比很高，下次还会买", 1),
    ("包装破损，非常失望", 0),
    ("物流很快，产品超出预期", 1),
    ("完全不值这个价格", 0),
    ("客服态度很好，解决了问题", 1),
    ("用了一天就坏了", 0),
    ("非常好用，强烈推荐", 1),
    ("垃圾产品，退货了", 0),
]

# 构建词表
def build_vocab(texts, min_freq=1):
    """构建词表（简化版，实际应用建议用 tokenizer）"""
    counter = Counter()
    for text, _ in texts:
        counter.update(list(text))  # 按字切分（中文简化处理）

    vocab = {"<pad>": 0, "<unk>": 1}
    for word, freq in counter.items():
        if freq >= min_freq:
            vocab[word] = len(vocab)
    return vocab

vocab = build_vocab(texts)
print(f"词表大小: {len(vocab)}")

class TextDataset(Dataset):
    def __init__(self, texts, vocab, max_len=50):
        self.data = []
        for text, label in texts:
            indices = [vocab.get(c, vocab["<unk>"]) for c in text]
            # 填充或截断到固定长度
            if len(indices) < max_len:
                indices += [vocab["<pad>"]] * (max_len - len(indices))
            else:
                indices = indices[:max_len]
            self.data.append((torch.tensor(indices), torch.tensor(label)))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

# ============================
# 2. 定义文本分类模型
# ============================
class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, hidden_dim=128, num_classes=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim,
            batch_first=True,
            bidirectional=True,
            dropout=0.3,
            num_layers=2
        )
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, 64),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        embedded = self.embedding(x)            # [batch, seq_len, embed_dim]
        output, (hidden, _) = self.lstm(embedded)
        # 使用最后时刻的隐状态
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.classifier(hidden)

# 初始化
dataset = TextDataset(texts, vocab)
loader = DataLoader(dataset, batch_size=4, shuffle=True)

model = TextClassifier(vocab_size=len(vocab)).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练
for epoch in range(50):
    model.train()
    total_loss = 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        output = model(x)
        loss = criterion(output, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}, Loss: {total_loss/len(loader):.4f}")

# 推理
model.eval()
with torch.no_grad():
    test_text = "这个产品很好用"
    indices = [vocab.get(c, vocab["<unk>"]) for c in test_text]
    indices += [0] * (50 - len(indices))
    x = torch.tensor([indices]).to(device)
    output = model(x)
    pred = output.argmax(dim=1).item()
    print(f"\n文本: '{test_text}'")
    print(f"预测: {'正面' if pred == 1 else '负面'}")
```

### 任务 5：模型部署为服务

```python
# inference_server.py
import torch
import torch.nn as nn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import io

app = FastAPI(title="图像分类推理服务")

# ============================
# 加载模型
# ============================
device = torch.device("cpu")  # 推理服务通常用 CPU（除非需要高吞吐）

# 加载保存的模型
# checkpoint = torch.load("best_mnist_model.pth", map_location=device)
# model = MNISTNet()
# model.load_state_dict(checkpoint)
# model.eval()

# ============================
# API 定义
# ============================
class PredictionInput(BaseModel):
    pixels: list[list[float]]  # 28x28 的像素值

class PredictionOutput(BaseModel):
    digit: int
    confidence: float
    all_probabilities: dict[str, float]

@app.post("/predict", response_model=PredictionOutput)
async def predict_digit(input_data: PredictionInput):
    """
    接收 28x28 的像素矩阵，返回数字分类结果

    类比 Web 开发：这就是一个普通的 POST API，
    只是处理逻辑从数据库查询变成了模型推理。
    """
    try:
        # 转换输入
        pixels = torch.tensor(input_data.pixels).unsqueeze(0).unsqueeze(0)
        pixels = pixels.float() / 255.0

        # 推理
        with torch.no_grad():
            output = torch.randn(1, 10)  # 模拟输出（实际用 model(pixels)）
            probabilities = torch.softmax(output, dim=1)[0]
            digit = probabilities.argmax().item()
            confidence = probabilities[digit].item()

        return PredictionOutput(
            digit=digit,
            confidence=round(confidence, 4),
            all_probabilities={
                str(i): round(p.item(), 4)
                for i, p in enumerate(probabilities)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
async def model_info():
    return {
        "model": "MNISTNet",
        "input_shape": [1, 28, 28],
        "output_classes": 10,
        "device": str(device)
    }

# 运行: uvicorn inference_server:app --reload --port 8001
```

## 实验记录模板

每次训练实验，建议用这个格式记录：

```markdown
## 实验：MNIST 全连接网络

### 配置
- 模型：3 层全连接 (784→256→128→10)
- 优化器：Adam, lr=0.001
- Batch Size：64
- Epochs：10

### 结果
| 指标 | 训练集 | 测试集 |
|------|--------|--------|
| 准确率 | 99.2% | 97.8% |
| 损失 | 0.025 | 0.072 |

### 观察
- 训练准确率和测试准确率差距不大，未出现严重过拟合
- 第 5 轮后准确率提升明显放缓
- Dropout 从 0.5 降到 0.2 后过拟合加剧

### 下一步
- 尝试 CNN 结构
- 增加数据增强
- 对比 SGD 和 Adam
```

## 建议实践

- 图像方向：手写数字、Fashion-MNIST、CIFAR-10
- 文本方向：情感分类、新闻分类、客服意图识别
- 实验追踪：至少保留准确率、损失和关键超参数

## 建议交付物

- 一份可重复训练的脚本或 Notebook
- 一组实验记录和调参说明
- 一个可访问的推理 Demo
- 一篇阶段总结，说明训练与部署踩坑

## 推荐资料

| 资料 | 类型 | 说明 |
|-----|------|------|
| PyTorch 官方教程 | 文档 | 最权威的入门指南 |
| fast.ai | 课程 | 自顶向下的实战教学 |
| CS231n | 课程 | 图像分类专题 |
| 《Dive into Deep Learning》第 2-8 章 | 书 | 理论 + 代码结合 |
| Hugging Face Course | 课程 | NLP 建模 |

## 配套工程建议

这一阶段通常会多出权重文件和实验日志，目录建议更明确：

```text
examples/learning/stage-3-deep-learning/
├─ README.md
├─ src/
│  ├─ 01_tensor_autograd.py
│  ├─ 02_mnist_classifier.py
│  ├─ 03_cifar10_cnn.py
│  ├─ 04_text_classifier.py
│  └─ 05_inference_server.py
├─ models/
│  ├─ best_mnist_model.pth
│  └─ best_cifar10_model.pth
├─ outputs/
│  └─ experiment_log.md
└─ configs/
   └─ train_config.yaml
```

如果暂时不做复杂配置管理，`configs/` 可以先不建，但最好尽早把超参数从脚本主体里拆出来。

## 常见误区

- 只会改网络层数，不理解训练循环和数据预处理
- 只看单次最好结果，不保留失败实验记录
- 部署时忽略模型加载时间、资源占用和输入校验
- 不清楚 `model.train()` 和 `model.eval()` 的区别（影响 Dropout 和 BatchNorm）
- 忘记 `torch.no_grad()` 导致推理时浪费内存

## 完成标准

- [ ] 能独立训练并保存一个可用模型
- [ ] 能解释模型效果受哪些因素影响
- [ ] 能把推理过程封装成一个最小服务
- [ ] 能写出完整的训练循环（前向、反向、更新、评估）
- [ ] 能说清 CNN 和全连接网络的区别
