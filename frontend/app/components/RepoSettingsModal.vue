<template>
  <UModal title="Repository Settings" v-model:open="open">
    <template #body>
      <div v-if="!confirmingDelete" class="flex flex-col gap-3">
        <UButton
            label="Reindex"
            :loading="loading"
            :disabled="loading"
            @click="handleReindex"
        />

        <UButton
            label="Remove"
            color="error"
            :disabled="loading"
            @click="confirmingDelete = true"
        />
      </div>

      <!-- CONFIRM DELETE STATE -->
      <div v-else class="flex flex-col gap-3">
        <p class="text-sm text-neutral-400">
          Are you sure you want to remove
          <strong>{{ repo?.name }}</strong>?
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

// reset state when modal opens
watch(open, (v) => {
  if (v) confirmingDelete.value = false
})
</script>