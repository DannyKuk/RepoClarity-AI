<template>
  <div>
    <div class="flex justify-between mb-3">
      <h2 class="font-semibold">Repositories</h2>

      <AddRepoModal
          v-model:open="modalOpen"
          :loading="loading"
          @add="handleAdd"
      />
    </div>

    <ul class="space-y-2">
      <RepoItem
          v-for="repo in repos"
          :key="repo.name"
          :repo="repo"
          @settings="(repo) => console.log('settings for', repo)"
      />
    </ul>

    <!-- alert -->
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
          @close="errorVisible = false"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
const modalOpen = ref(false)

const {
  repos,
  loading,
  errorVisible,
  fetchRepos,
  addRepo
} = useRepos()

onMounted(fetchRepos)

async function handleAdd({ name, path }: { name: string; path: string }) {
  const success = await addRepo(name, path)

  if (success) {
    modalOpen.value = false
  }
}

watch(modalOpen, (v) => {
  if (v) {
    errorVisible.value = false
  }
})

watch(errorVisible, (v) => {
  if (v) {
    setTimeout(() => {
      errorVisible.value = false
    }, 4000)
  }
})
</script>