---
layout: page
---
<script setup>
import {
  VPTeamPage,
  VPTeamPageTitle,
  VPTeamMembers
} from 'vitepress/theme'

const members = [
  {
    avatar: 'https://github.com/moustafa-shaaban.png',
    name: 'Moustafa',
    title: 'Creator',
    links: [
      { icon: 'github', link: 'https://github.com/moustafa-shaaban' },
    ]
  },
]
</script>

<VPTeamPage>
  <VPTeamPageTitle>
    <template #title>
      Built By
    </template>
    <!-- <template #lead>
      The development of VitePress is guided by an international
      team, some of whom have chosen to be featured below.
    </template> -->
  </VPTeamPageTitle>
  <VPTeamMembers :members />
</VPTeamPage>