<template>
  <UModal title="Repository Settings" v-model:open="open">
    <template #body>
      <div class="flex flex-col gap-3">
        <UButton
            label="Reindex"
            :loading="loading"
            :disabled="loading"
            @click="handleReindex"
        />

        <UButton
            label="Remove"
            color="error"
            :loading="loading"
            :disabled="loading"
            @click="handleDelete"
        />
      </div>
    </template>
  </UModal>
</template>

<script setup lang="ts">
import type { Repo } from "~/types/api"

const open = defineModel<boolean>('open')

const props = defineProps<{
  repo: Repo | null
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'reindex', repo: Repo): void
  (e: 'delete', repo: Repo): void
}>()

function handleReindex() {
  if (props.repo) emit('reindex', props.repo)
}

function handleDelete() {
  if (props.repo) emit('delete', props.repo)
}
</script>