<template>
  <div
      class="flex"
      :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
      data-test="message"
  >
    <div 
        class="max-w-[85%] rounded-2xl px-5 py-4 shadow-sm transition-all"
        :class="message.role === 'user' 
          ? 'bg-gradient-to-br from-primary-600 to-purple-600 text-white rounded-br-sm shadow-[0_4px_14px_rgba(59,130,246,0.25)]' 
          : 'bg-neutral-900/60 backdrop-blur-md border border-neutral-800/50 rounded-tl-sm text-neutral-200'"
    >
      <div 
        data-test="message-role" 
        class="mb-2 flex items-center gap-2"
      >
        <div v-if="message.role !== 'user'" class="w-5 h-5 rounded bg-primary-500/20 flex items-center justify-center border border-primary-500/30">
          <UIcon name="lucide:bot" class="text-primary-400 w-3 h-3" />
        </div>
        <span class="text-xs font-semibold tracking-wider uppercase opacity-70">
          {{ message.role === 'user' ? 'You' : 'RepoClarity' }}
        </span>
      </div>

      <!-- User -->
      <div v-if="message.role === 'user'" data-test="message-text" class="text-[15px] leading-relaxed">
        {{ message.text }}
      </div>

      <!-- Assistant -->
      <div v-else class="text-[15px] leading-relaxed">

        <div v-if="message.languages?.length || message.framework" class="flex flex-wrap gap-2 mb-4">
          <div v-for="l in message.languages" :key="l">
            <UBadge variant="subtle" color="primary" class="rounded-lg shadow-sm border border-primary-500/20">{{ l }}</UBadge>
          </div>
          <div v-if="message.framework">
            <UBadge variant="subtle" color="purple" class="rounded-lg shadow-sm border border-purple-500/20">{{ message.framework }}</UBadge>
          </div>
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

        <div v-if="message.sources?.length" class="mt-4 flex flex-wrap gap-2 pt-4 border-t border-neutral-800/50">
          <div v-for="s in message.sources" :key="s.path + '-' + s.start" data-test="sources">
            <UBadge variant="soft" color="gray" class="font-mono text-[10px] rounded border border-neutral-700/50 hover:bg-neutral-800 transition-colors">
              <UIcon name="lucide:file-code-2" class="w-3 h-3 mr-1" />
              {{ formatSource(s) }}
            </UBadge>
          </div>
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