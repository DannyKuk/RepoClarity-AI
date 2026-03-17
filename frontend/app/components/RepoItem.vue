<template>
  <li>
    <div class="flex items-center gap-2">
      <NuxtLink
          :to="`/repo/${repo.name}`"
          class="flex-1 block p-2 rounded hover:bg-neutral-800"
      >
        <div class="flex justify-between items-center">
          <span>{{ repo.name }}</span>

          <UBadge
              v-if="repo.framework"
              size="sm"
              color="secondary"
              variant="outline"
          >
            {{ repo.framework }}
          </UBadge>
        </div>
      </NuxtLink>

      <UButton
          icon="i-lucide-settings"
          size="sm"
          variant="ghost"
          @click="$emit('settings', repo)"
      />
    </div>

    <USeparator class="my-1" />
  </li>
</template>

<script setup lang="ts">
import type { Repo } from "~/types/api"

defineProps<{ repo: Repo }>()
defineEmits<{
  (e: 'settings', repo: Repo): void
}>()
</script>