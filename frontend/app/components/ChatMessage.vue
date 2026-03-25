<template>
  <div
      class="flex"
      :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
      data-test="message"
  >
    <div class="max-w-[65%] rounded-2xl bg-neutral-800 px-4 py-3 shadow-sm">

      <div data-test="message-role">
        {{ message.role === 'user' ? 'You' : 'RepoClarity' }}
      </div>

      <!-- User -->
      <div v-if="message.role === 'user'" data-test="message-text">
        {{ message.text }}
      </div>

      <!-- Assistant -->
      <div v-else class="mt-2 border-t-2 border-neutral-700">

        <div v-if="message.languages?.length" data-test="sources" class="flex flex-row mt-3 gap-1">
          <div v-for="l in message.languages" :key="l"><UBadge variant="outline" color="secondary">{{ l }}</UBadge></div>
        </div>
        <div v-if="message.framework" data-test="framework" class="mb-2 mt-1">
          <UBadge color="neutral" variant="outline">{{ message.framework }}</UBadge>
        </div>

        <div v-if="!message.blocks" data-test="message-text">
          {{ message.text }}
        </div>

        <template v-for="(block, i) in message.blocks" :key="i">

          <div
              v-if="block.type === 'markdown'"
              data-test="markdown"
              v-html="block.html"
          />

          <CodeBlock
              v-else
              data-test="code-block"
              :code="block.code"
              :language="block.lang"
          />

        </template>

        <div v-for="s in message.sources" :key="s.path + '-' + s.start" data-test="sources">
          <UBadge variant="outline">
            {{ formatSource(s) }}
          </UBadge>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import CodeBlock from '@/components/CodeBlock.vue'
import type { ChatMessageType } from "~/types/api";

defineProps<{
  message: ChatMessageType
}>()

function formatSource(s: { path: string; start?: number; end?: number }) {
  if (s.start != null && s.end != null) {
    return `${s.path} (lines ${s.start}-${s.end})`
  }
  return s.path
}
</script>