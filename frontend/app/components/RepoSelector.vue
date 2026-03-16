<template>
  <div>
    <h2 class="font-semibold mb-3">Repositories</h2>

    <ul class="space-y-2">
      <li
          v-for="repo in repos"
          :key="repo.name"
      >
        <NuxtLink
            :to="`/repo/${repo.name}`"
            class="block p-2 rounded hover:bg-neutral-800"
        >
          {{ repo.name }}
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { getRepos } from "~/composables/api";

const repos = ref<any[]>([])

onMounted(async () => {
  repos.value = await getRepos()
})
</script>