import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base: '/Map-It/',
  title: "Map-It Documentation",
  description: "Map-It Documentation",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      {
        text: 'Applications',
        items: [
          { text: 'Applications', link: '/applications' },
          { text: 'Seattle', link: '/applications/seattle' },
          { text: 'Item B', link: '/item-2' },
        ]
      },
      { text: 'Examples', link: '/markdown-examples' },
      { text: 'Team', link: '/team' },
    ],

    sidebar: [
      {
        text: 'Applications',
        items: [
          { text: 'Applications', link: '/applications' },
          { text: 'Seattle', link: '/applications/seattle' },
          { text: 'Item B', link: '/item-2' },
        ]
      },
      {
        text: 'Examples',
        items: [
          { text: 'Markdown Examples', link: '/markdown-examples' },
          { text: 'Runtime API Examples', link: '/api-examples' }
        ]
      },
      { text: 'Team', link: '/team' },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/moustafa-shaaban/Map-It' }
    ],
    search: {
      provider: 'local'
    },
    lastUpdated: true,
    lastUpdated: {
      text: 'Updated at',
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'medium'
      }
    },
  }
})
