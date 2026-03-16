<template>
  <UApp>
    <NuxtLayout>
      <NuxtRouteAnnouncer />
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>

<script setup lang="ts">
const modelsStore = useModelsStore()

await callOnce(() => modelsStore.fetchModels())
</script>