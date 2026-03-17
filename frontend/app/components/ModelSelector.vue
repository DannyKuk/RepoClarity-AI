<template>
  <div class="flex gap-3 mb-3">
    <USelect placeholder="default" variant="soft" v-model="model" :items="models" class="w-52"/>

    <UButton
        color="secondary"
        variant="soft"
        icon="i-lucide-refresh-cw"
        :loading="loading"
        @click="modelsStore.reloadModels()"
    />
  </div>
</template>

<script setup lang="ts">
const model = defineModel<string>()

const modelsStore = useModelsStore()
const { models, loading } = storeToRefs(modelsStore)
</script>