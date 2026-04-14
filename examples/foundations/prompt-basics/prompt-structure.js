const prompt = {
  system: '你是一个帮助用户整理 AI 学习笔记的助手。',
  task: '把输入内容整理成结构化学习笔记。',
  constraints: [
    '不要编造事实',
    '不确定的信息要标记为待确认',
    '输出尽量简洁'
  ],
  outputFormat: ['Summary', 'Key Concepts', 'Examples', 'Open Questions']
}

function renderPrompt(config) {
  return [
    `System: ${config.system}`,
    `Task: ${config.task}`,
    'Constraints:',
    ...config.constraints.map((item, index) => `${index + 1}. ${item}`),
    'Output Format:',
    ...config.outputFormat.map((item, index) => `${index + 1}. ${item}`)
  ].join('\n')
}

console.log(renderPrompt(prompt))
