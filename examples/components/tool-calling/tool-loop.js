const tools = {
  searchDocs(query) {
    const docs = [
      'Prompt 用来约束任务目标和输出格式。',
      'RAG 常用于接入外部知识。',
      'Tool calling 适合获取最新信息或执行确定性动作。'
    ]

    return docs.filter((item) => item.toLowerCase().includes(query.toLowerCase()))
  },
  calculate(expression) {
    return Function(`"use strict"; return (${expression})`)()
  }
}

function chooseTool(userInput) {
  if (userInput.includes('文档')) {
    return { name: 'searchDocs', args: ['tool'] }
  }

  if (userInput.includes('计算')) {
    return { name: 'calculate', args: ['12 * 8'] }
  }

  return null
}

function run(userInput) {
  const toolCall = chooseTool(userInput)

  if (!toolCall) {
    return '当前问题不需要工具，直接由模型回答即可。'
  }

  const result = tools[toolCall.name](...toolCall.args)
  return {
    tool: toolCall.name,
    args: toolCall.args,
    result
  }
}

console.log(JSON.stringify(run('请帮我查一下和 tool calling 相关的文档'), null, 2))
console.log(JSON.stringify(run('请帮我计算一个结果'), null, 2))
