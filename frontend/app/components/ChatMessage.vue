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
      <div v-else>

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

        <div v-if="message.framework" data-test="framework">
          {{ message.framework }}
        </div>

        <div v-if="message.sources?.length" data-test="sources">
          <div v-for="s in message.sources" :key="s">{{ s }}</div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import CodeBlock from '@/components/CodeBlock.vue'

defineProps<{
  message: any
}>()
</script>