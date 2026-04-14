const knowledgeBase = [
  {
    id: 'doc-1',
    text: 'Prompt engineering 关注任务描述、约束条件和输出格式。'
  },
  {
    id: 'doc-2',
    text: 'RAG 通常包括切分、索引、召回和生成四个主要步骤。'
  },
  {
    id: 'doc-3',
    text: 'Agent 需要目标、状态、工具和停止条件。'
  }
]

function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s]/gu, ' ')
    .split(/\s+/)
    .filter(Boolean)
}

function score(query, doc) {
  const queryTokens = new Set(tokenize(query))
  const docTokens = tokenize(doc.text)
  return docTokens.reduce((total, token) => total + (queryTokens.has(token) ? 1 : 0), 0)
}

function retrieve(query, topK = 2) {
  return knowledgeBase
    .map((doc) => ({ ...doc, score: score(query, doc) }))
    .filter((doc) => doc.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, topK)
}

const query = '我想理解 RAG 的主要步骤'
console.log(JSON.stringify({ query, matches: retrieve(query) }, null, 2))
