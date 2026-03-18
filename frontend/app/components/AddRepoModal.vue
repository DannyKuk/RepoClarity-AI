<template>
  <UModal title="Add Repository" v-model:open="open">
    <template #default>
      <UButton
          icon="i-lucide-plus"
          size="sm"
          @click="open = true"
      />
    </template>

    <template #body>
      <div class="flex flex-col gap-2 mb-5">
        <UInput placeholder="Source Path" v-model="repoSourcePath" />
        <UInput placeholder="Name" v-model="repoName" />
      </div>

      <div class="flex justify-end gap-2">
        <UButton
            label="Cancel"
            variant="outline"
            color="error"
            @click="open = false"
            :disabled="loading"
        />

        <UButton
            label="Add"
            variant="outline"
            :loading="loading"
            :disabled="loading"
            @click="handleSubmit"
        />
      </div>
    </template>
  </UModal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const open = defineModel<boolean>('open')

const props = defineProps<{
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'add', payload: { name: string; path: string }): void
}>()

const repoName = ref('')
const repoSourcePath = ref('')

function handleSubmit() {
  if (!repoName.value || !repoSourcePath.value) return

  emit('add', {
    name: repoName.value,
    path: repoSourcePath.value
  })
}

watch(() => open.value, (v) => {
  if (v) {
    repoName.value = ''
    repoSourcePath.value = ''
  }
})
</script>