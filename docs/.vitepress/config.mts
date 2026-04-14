import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: 'Awesome AI',
  description: '个人 AI 知识库、实验记录与最小示例。',
  base: '/awesome-ai/',
  vite: {
    server: {
      port: 8087
    }
  },
  cleanUrls: true,
  lastUpdated: true,
  head: [
    ['meta', { name: 'theme-color', content: '#0f766e' }],
    ['meta', { name: 'author', content: 'hwlv' }],
    ['link', { rel: 'icon', href: '/favicon.svg' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'Awesome AI' }],
    ['meta', { property: 'og:description', content: '个人 AI 知识库、实验记录与最小示例。' }]
  ],
  themeConfig: {
    siteTitle: 'Awesome AI',
    logo: '/favicon.svg',
    search: {
      provider: 'local'
    },
    nav: [
      { text: '开始', link: '/guide/start-here' },
      { text: '学习路径', link: '/learning/' },
      { text: '概念基础', link: '/foundations/' },
      { text: '能力模块', link: '/components/' },
      { text: '系统搭建', link: '/systems/' },
      { text: '实战项目', link: '/practice/' },
      { text: '资料库', link: '/resources/' }
    ],
    sidebar: {
      '/guide/': [
        {
          text: '开始',
          items: [
            { text: '从这里开始', link: '/guide/start-here' },
            { text: '知识地图与目录结构', link: '/guide/knowledge-architecture' },
            { text: 'AI 知识树（建议版）', link: '/guide/ai-knowledge-tree' },
            { text: '站点路线图', link: '/guide/site-roadmap' }
          ]
        }
      ],
      '/learning/': [
        {
          text: '学习路径',
          items: [
            { text: '学习路径总览', link: '/learning/' },
            { text: 'Web 开发者转 AI 学习路线', link: '/learning/web-developer-to-ai-roadmap' },
            { text: '阶段 1：Python 与数学基础', link: '/learning/python-math-basics' },
            { text: '阶段 2：经典机器学习', link: '/learning/classical-ml' },
            { text: '阶段 3：深度学习核心', link: '/learning/deep-learning-core' },
            { text: '阶段 4：AI + Web 产品化', link: '/learning/ai-web-product' }
          ]
        }
      ],
      '/foundations/': [
        {
          text: '概念基础',
          items: [
            { text: '总览', link: '/foundations/' },
            { text: 'AI 基本概念总览', link: '/foundations/ai-basics' },
            { text: '模型 API 调用入门', link: '/foundations/model-api-access' }
          ]
        }
      ],
      '/components/': [
        {
          text: '能力模块',
          items: [
            { text: '总览', link: '/components/' },
            { text: 'Prompt 基础', link: '/components/prompting' },
            { text: 'Embeddings 与 RAG', link: '/components/embeddings-rag' },
            { text: 'Tool Calling', link: '/components/tool-calling' }
          ]
        }
      ],
      '/systems/': [
        {
          text: '系统搭建',
          items: [
            { text: '总览', link: '/systems/' },
            { text: 'Agent 基础', link: '/systems/agent-basics' },
            { text: 'Agent 模式与拆解', link: '/systems/agent-patterns' },
            { text: 'Agent 优先工程化', link: '/systems/agent-first-engineering' },
            { text: '利用 Codex 的工程技术笔记', link: '/systems/harness-engineering-notes' }
          ]
        }
      ],
      '/practice/': [
        {
          text: '实战项目',
          items: [
            { text: '实战总览', link: '/practice/' }
          ]
        }
      ],
      '/resources/': [
        {
          text: '资料库',
          items: [
            { text: '总览', link: '/resources/' },
            { text: '精选参考资料', link: '/resources/curated-resources' },
            { text: '常用 Skill 清单', link: '/resources/playbooks/common-skills' },
            { text: '提示词模板', link: '/resources/playbooks/prompt-templates' },
            { text: '自主循环 Prompt', link: '/resources/playbooks/autonomous-loop-prompt' },
            { text: '阅读笔记：陶哲轩谈 AI 科学革命', link: '/resources/reading-notes/tao-ai-science-revolution' },
            { text: '每周复盘模板', link: '/resources/reviews/weekly-review' },
            { text: '知识笔记模板', link: '/resources/templates/knowledge-note' },
            { text: '资料卡片模板', link: '/resources/templates/resource-note' }
          ]
        }
      ],
      '/archive/': [
        {
          text: '归档',
          items: [
            { text: '归档说明', link: '/archive/' },
            { text: 'AI 概念笔记', link: '/archive/ai概念' },
            { text: 'LLM 学习路径（旧版摘录）', link: '/archive/llm学习路径' },
            { text: '日报（归档）', link: '/archive/日报' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/hwlv/awesome-ai' }
    ],
    outline: {
      level: [2, 3],
      label: '本页导航'
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    lastUpdated: {
      text: '最近更新于'
    },
    footer: {
      message: 'Built with VitePress and deployed via GitHub Actions.',
      copyright: 'Copyright © 2026 hwlv'
    }
  }
})
