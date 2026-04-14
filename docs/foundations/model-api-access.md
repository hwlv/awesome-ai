# 模型 API 调用入门

很多 AI 项目的第一步，不是训练模型，而是先把外部模型服务稳定接起来。

这件事看起来只是“发个 HTTP 请求”，但真正决定后面工程质量的，往往就是这里的边界设计。

## 一次模型调用通常包含什么

- 接口地址：你要调用哪个服务
- 鉴权方式：API Key、Token 或其他签名
- 模型标识：具体使用哪个模型
- 输入消息：system、user、tool 等上下文
- 推理参数：例如温度、最大输出长度
- 错误处理：超时、限流、参数错误、供应商异常

## 一个安全的最小原则

### 不要把密钥写进仓库

把密钥直接写进 Markdown、脚本或前端代码里，后面几乎一定会出问题。

优先使用环境变量：

```bash
export MODEL_API_KEY="your-secret"
```

### 不要把供应商细节写死在业务层

最好把“发请求”封成单独模块，避免后面换模型供应商时到处改代码。

## `curl` 示例

下面是一个安全版示意，保留了“聊天补全”这类常见调用结构，但不把真实密钥写死：

```bash
curl -X POST "https://open.bigmodel.cn/api/paas/v4/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: ${MODEL_API_KEY}" \
  -d '{
    "model": "YOUR_MODEL_ID",
    "messages": [
      {
        "role": "user",
        "content": "请给这个产品写一句简洁口号"
      }
    ],
    "max_tokens": 1024,
    "temperature": 0.7
  }'
```

如果你接的是别家服务，也建议保持同样的结构化思路：

- endpoint 独立配置
- key 从环境变量读取
- model id 单独配置
- 请求和响应各有明确类型

## 工程上要尽快补的东西

- 超时和重试策略
- 限流和错误码映射
- 请求日志和调用成本统计
- 供应商切换或降级能力

## 常见错误

- 把 API Key 直接提交到仓库
- 在前端直接暴露供应商凭证
- 模型名称、地址、参数散落在各处
- 只考虑“调通”，没有考虑失败时怎么退化

## 和站点其他内容的关系

- 如果你在做工具调用或工作流编排，可以继续看 [Tool Calling](/components/tool-calling)
- 如果你在做产品化接入，可以继续看 [阶段 4：AI + Web 产品化](/learning/ai-web-product)
