<template>
  <UModal title="Repository Settings" v-model:open="open">
    <template #body>
      <div class="flex flex-col gap-4">
        <!-- context -->
        <p class="text-sm text-neutral-400">
          Managing <strong>{{ repo?.name }}</strong>
        </p>

        <!-- NORMAL STATE -->
        <div v-if="!confirmingDelete" class="flex flex-col gap-3">
          <!-- REINDEX -->
          <div class="flex items-center justify-between">
            <span class="text-sm text-neutral-300">
              Rebuild embeddings for this repository
            </span>

            <UButton
                label="Reindex"
                size="sm"
                variant="outline"
                icon="i-lucide-refresh-cw"
                :loading="loading"
                :disabled="loading"
                @click="handleReindex"
            />
          </div>

          <!-- divider -->
          <div class="border-t border-neutral-800" />

          <!-- DELETE -->
          <div class="flex items-center justify-between">
            <span class="text-sm text-neutral-300">
              Permanently delete repo and index
            </span>

            <UButton
                label="Remove"
                size="sm"
                color="error"
                variant="outline"
                icon="i-lucide-trash"
                :disabled="loading"
                @click="confirmingDelete = true"
            />
          </div>
        </div>

        <!-- CONFIRM DELETE -->
        <div v-else class="flex flex-col gap-3">
          <p class="text-sm text-neutral-400">
            This will permanently remove
            <strong>{{ repo?.name }}</strong> and its index.
            This action cannot be undone.
          </p>

          <div class="flex justify-end gap-2">
            <UButton
                label="Cancel"
                variant="outline"
                @click="confirmingDelete = false"
                :disabled="loading"
            />

            <UButton
                label="Yes, remove"
                color="error"
                :loading="loading"
                :disabled="loading"
                @click="handleDelete"
            />
          </div>
        </div>
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

const confirmingDelete = ref(false)

function handleReindex() {
  if (props.repo) emit('reindex', props.repo)
}

function handleDelete() {
  if (props.repo) emit('delete', props.repo)
}

watch(open, (v) => {
  if (v) confirmingDelete.value = false
})
</script>