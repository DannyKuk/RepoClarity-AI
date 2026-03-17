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
            <UButton
                label="Add"
                variant="outline"
                @click="addRepo"
                :loading="loading"
            />
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
          <div class="flex justify-between">
            {{ repo.name }}
            <UBadge v-if="repo.framework" size="sm" variant="outline" color="secondary">{{ repo.framework }}</UBadge>
          </div>
        </NuxtLink>
        <USeparator class="my-1"/>
      </li>
    </ul>

    <!-- Bottom alert -->
    <div
        v-if="errorVisible"
        class="fixed bottom-4 left-[5%] w-[90vw] z-50"
    >
      <UAlert
          color="error"
          variant="soft"
          title="Failed to index repository"
          description="Check that the repository path exists and the backend can access it."
          icon="i-lucide-alert-circle"
          :close-button="{ icon: 'i-lucide-x' }"
      />
    </div>
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
const errorVisible = ref(false)

async function addRepo() {
  const config = useRuntimeConfig()

  loading.value = true
  errorVisible.value = false

  try {
    await $fetch(`${config.public.apiBase}/repos/index`, {
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
    loading.value = false
    errorVisible.value = true
  }
}

onMounted(async () => {
  repos.value = await getRepos()
})

watch(modalOpen, (v) => {
  if (v) errorVisible.value = false
})
</script>