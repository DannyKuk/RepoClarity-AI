<template>
  <div>
    <div class="flex flex-row justify-between mb-3">
      <h2 class="font-semibold">Repositories</h2>

      <UModal title="Add Repository" v-model:open="modalOpen">
        <UButton
            icon="i-lucide-plus"
            size="sm"
            color="neutral"
            variant="solid"
            @click="modalOpen = true"
        />

        <template #body>
          <div class="flex flex-col gap-2 mb-5">
            <UInput placeholder="Source Path" v-model="repoSourcePath" />
            <UInput placeholder="Name" v-model="repoName" />
          </div>

          <div class="flex flex-row gap-2 justify-end">
            <UButton
                label="Cancel"
                color="error"
                variant="outline"
                @click="modalOpen = false"
                :loading="loading"
            />
            <UButton label="Add" variant="outline" @click="addRepo" :loading="loading"/>
          </div>
        </template>
      </UModal>
    </div>

    <ul class="space-y-2">
      <li v-for="repo in repos" :key="repo.name">
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
import { getRepos } from "~/composables/api"
import type { Repo } from "~/types/api"

const repos = ref<Repo[]>([])
const repoSourcePath = ref('')
const repoName = ref('')
const modalOpen = ref(false)
const loading = ref(false)

async function addRepo() {
  loading.value = true
  try {
    await $fetch('http://localhost:8000/repos/index', {
      method: 'POST',
      body: {
        name: repoName.value,
        path: repoSourcePath.value
      }
    })

    repos.value = await getRepos()

    repoName.value = ''
    repoSourcePath.value = ''

    modalOpen.value = false
  } catch (err) {
    console.error('Failed to index repo', err)
  }
  loading.value = false
}

onMounted(async () => {
  repos.value = await getRepos()
})
</script>