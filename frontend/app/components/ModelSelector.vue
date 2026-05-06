<template>
  <div class="flex gap-3 mb-6 items-center">
    <div class="text-xs font-medium uppercase tracking-wider text-neutral-500">Model:</div>
    <USelect placeholder="Select a model" variant="soft" color="primary" v-model="model" :items="models" class="w-56 shadow-sm"/>

    <UButton
        color="gray"
        variant="ghost"
        icon="i-lucide-refresh-cw"
        :loading="loading"
        :disabled="loading"
        @click="modelsStore.reloadModels()"
        class="hover:bg-neutral-800/50 rounded-lg"
    />
  </div>
</template>

<script setup lang="ts">
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'

const model = defineModel<string>()

const modelsStore = useModelsStore()
const { models, loading } = storeToRefs(modelsStore)
</script>