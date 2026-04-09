"""
阶段 3 - 脚本 2：MNIST 手写数字识别
完整的训练→评估→保存流程
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import time

# ============================================================
# 1. 配置
# ============================================================
print("=" * 60)
print("MNIST 手写数字识别")
print("=" * 60)

BATCH_SIZE = 64
EPOCHS = 5  # 演示用，实际可增大
LR = 0.001

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "mps" if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available()
    else "cpu"
)
print(f"设备: {device}")

# ============================================================
# 2. 数据加载
# ============================================================
print("\n加载 MNIST 数据集...")

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST("./data", train=True, download=True, transform=transform)
test_dataset = datasets.MNIST("./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

print(f"训练集: {len(train_dataset)} 张图")
print(f"测试集: {len(test_dataset)} 张图")
print(f"图片尺寸: {train_dataset[0][0].shape}")

# ============================================================
# 3. 定义网络
# ============================================================
class MNISTNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.layers = nn.Sequential(
            nn.Linear(28 * 28, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.layers(x)

model = MNISTNet().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

params = sum(p.numel() for p in model.parameters())
print(f"\n模型参数量: {params:,}")

# ============================================================
# 4. 训练
# ============================================================
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, correct, total = 0, 0, 0
    for data, target in loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        loss = criterion(output, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        correct += output.argmax(1).eq(target).sum().item()
        total += target.size(0)
    return total_loss / len(loader), correct / total

def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss, correct, total = 0, 0, 0
    with torch.no_grad():
        for data, target in loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            total_loss += criterion(output, target).item()
            correct += output.argmax(1).eq(target).sum().item()
            total += target.size(0)
    return total_loss / len(loader), correct / total

print(f"\n{'Epoch':>5} | {'Train Loss':>10} | {'Train Acc':>9} | "
      f"{'Test Loss':>9} | {'Test Acc':>8} | {'Time':>6}")
print("-" * 65)

best_acc = 0
start_total = time.time()

for epoch in range(1, EPOCHS + 1):
    start = time.time()
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
    test_loss, test_acc = evaluate(model, test_loader, criterion, device)
    elapsed = time.time() - start

    print(f"{epoch:>5} | {train_loss:>10.4f} | {train_acc:>8.2%} | "
          f"{test_loss:>9.4f} | {test_acc:>7.2%} | {elapsed:>5.1f}s")

    if test_acc > best_acc:
        best_acc = test_acc
        torch.save(model.state_dict(), "models/best_mnist_model.pth")

total_time = time.time() - start_total
print(f"\n总训练时间: {total_time:.1f}s")
print(f"最优测试准确率: {best_acc:.2%}")

# ============================================================
# 5. 推理演示
# ============================================================
print("\n" + "=" * 60)
print("推理演示")
print("=" * 60)

model.eval()
with torch.no_grad():
    # 取前 10 张测试图
    data, target = next(iter(test_loader))
    data, target = data[:10].to(device), target[:10]
    output = model(data)
    pred = output.argmax(dim=1)
    probs = torch.softmax(output, dim=1)

    print(f"\n{'序号':>4} | {'真实':>4} | {'预测':>4} | {'置信度':>6} | {'结果'}")
    print("-" * 40)
    for i in range(10):
        confidence = probs[i][pred[i]].item()
        correct = "✅" if pred[i].item() == target[i].item() else "❌"
        print(f"{i+1:>4} | {target[i].item():>4} | {pred[i].item():>4} | "
              f"{confidence:>5.1%} | {correct}")

print("\n✅ MNIST 训练完成！")
