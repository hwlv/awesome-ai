const state = {
  goal: '写出一份关于 AI 知识库建设的最小计划',
  notes: [],
  completed: false
}

function decideNextStep(currentState) {
  if (currentState.notes.length === 0) {
    return 'collect_topics'
  }

  if (currentState.notes.length < 3) {
    return 'refine_outline'
  }

  return 'finish'
}

function act(action, currentState) {
  if (action === 'collect_topics') {
    currentState.notes.push('确定栏目：fundamentals、skills、agents、references。')
    return
  }

  if (action === 'refine_outline') {
    currentState.notes.push('给每个栏目补 1 到 2 篇起步文档。')
    currentState.notes.push('为每个核心主题准备一个最小示例。')
    return
  }

  if (action === 'finish') {
    currentState.completed = true
  }
}

while (!state.completed) {
  const nextAction = decideNextStep(state)
  act(nextAction, state)
}

console.log(JSON.stringify(state, null, 2))
