import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: 'Awesome AI',
  description: '个人 AI 知识库、实验记录与最小示例。',
  base: '/awesome-ai/',
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
      { text: '基础概念', link: '/fundamentals/ai-basics' },
      { text: 'Skills', link: '/skills/common-skills' },
      { text: 'Agents', link: '/agents/agent-basics' },
      { text: '示例', link: '/examples/' },
      { text: '参考资料', link: '/references/curated-resources' }
    ],
    sidebar: {
      '/guide/': [
        {
          text: 'Guide',
          items: [
            { text: '从这里开始', link: '/guide/start-here' },
            { text: '站点路线图', link: '/guide/site-roadmap' }
          ]
        }
      ],
      '/learning/': [
        {
          text: 'Learning',
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
      '/fundamentals/': [
        {
          text: 'Fundamentals',
          items: [
            { text: 'AI 基本概念总览', link: '/fundamentals/ai-basics' },
            { text: 'Prompt 基础', link: '/fundamentals/prompting' },
            { text: 'Embeddings 与 RAG', link: '/fundamentals/embeddings-rag' },
            { text: 'Tool Calling', link: '/fundamentals/tool-calling' },
            { text: '模型 API 调用入门', link: '/fundamentals/model-api-access' }
          ]
        }
      ],
      '/skills/': [
        {
          text: 'Skills',
          items: [
            { text: '常用 Skill 清单', link: '/skills/common-skills' },
            { text: '提示词模板', link: '/skills/prompt-templates' },
            { text: '自主循环 Prompt', link: '/skills/autonomous-loop-prompt' }
          ]
        }
      ],
      '/agents/': [
        {
          text: 'Agents',
          items: [
            { text: 'Agent 基础', link: '/agents/agent-basics' },
            { text: 'Agent 模式与拆解', link: '/agents/agent-patterns' },
            { text: 'Agent 优先工程化', link: '/agents/agent-first-engineering' },
            { text: '利用 Codex 的工程技术笔记', link: '/agents/harness-engineering-notes' }
          ]
        }
      ],
      '/references/': [
        {
          text: 'References',
          items: [
            { text: '精选参考资料', link: '/references/curated-resources' }
          ]
        }
      ],
      '/reviews/': [
        {
          text: 'Reviews',
          items: [
            { text: '每周复盘模板', link: '/reviews/weekly-review' }
          ]
        }
      ],
      '/templates/': [
        {
          text: 'Templates',
          items: [
            { text: '知识笔记模板', link: '/templates/knowledge-note' },
            { text: '资料卡片模板', link: '/templates/resource-note' }
          ]
        }
      ],
      '/examples/': [
        {
          text: 'Examples',
          items: [
            { text: '示例总览', link: '/examples/' }
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
