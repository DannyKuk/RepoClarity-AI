<template>
  <li>
    <div class="flex items-center gap-2">
      <NuxtLink
          :to="`/repo/${repo.name}`"
          class="flex-1 block p-2.5 rounded-xl hover:bg-neutral-800/50 transition-colors border border-transparent hover:border-neutral-700/50"
          active-class="bg-primary-900/20 border-primary-500/30 text-primary-400 hover:bg-primary-900/30 hover:border-primary-500/40"
      >
        <div class="flex justify-between items-center">
          <span>{{ repo.name }}</span>

          <UBadge
              v-if="repo.languages?.length"
              size="sm"
              color="primary"
              variant="subtle"
              class="text-[10px] uppercase tracking-wider"
          >
            {{ repo.languages[0] }}
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

    <USeparator class="my-1 opacity-50" />
  </li>
</template>

<script setup lang="ts">
import type { Repo } from "~/types/api"

defineProps<{ repo: Repo }>()
defineEmits<{
  (e: 'settings', repo: Repo): void
}>()
</script>