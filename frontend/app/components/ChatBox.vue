<template>
  <div class="flex h-full min-h-[75vh] flex-col gap-4">

    <!-- Messages -->
    <div
        ref="messagesContainer"
        data-test="messages-container"
        class="flex-1 min-h-[75vh] max-h-[75vh] space-y-6 overflow-y-auto rounded-2xl border border-neutral-800/60 bg-neutral-950/40 backdrop-blur-md p-6 shadow-xl shadow-black/20 relative scroll-smooth"
    >
      <!-- Empty state -->
      <div
          v-if="messages.length === 0"
          data-test="empty-state"
          class="flex h-full min-h-75 items-center justify-center text-sm text-neutral-500"
      >
        Ask something about
        <span class="mx-1 font-semibold text-neutral-300">{{ repo }}</span>.
      </div>

      <!-- Messages -->
      <ChatMessage
          v-for="message in messages"
          :key="message.id"
          :message="message"
      />

      <!-- Loading -->
      <div v-if="loading" data-test="loading" class="flex justify-start">
        <div class="max-w-[85%] rounded-2xl border border-primary-900/50 bg-primary-950/20 backdrop-blur-sm px-5 py-4 shadow-[0_0_15px_rgba(59,130,246,0.1)]">
          <div class="mb-3 flex items-center gap-2">
            <div class="w-6 h-6 rounded-md bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center">
              <UIcon name="lucide:bot" class="text-white w-3 h-3" />
            </div>
            <span class="text-xs font-semibold uppercase tracking-wider text-primary-400">RepoClarity</span>
          </div>
          <div class="flex items-center gap-3 text-sm text-neutral-300">
            <div class="flex gap-1">
              <span class="h-1.5 w-1.5 animate-bounce rounded-full bg-primary-500" style="animation-delay: 0s" />
              <span class="h-1.5 w-1.5 animate-bounce rounded-full bg-primary-500" style="animation-delay: 0.2s" />
              <span class="h-1.5 w-1.5 animate-bounce rounded-full bg-primary-500" style="animation-delay: 0.4s" />
            </div>
            Thinking...
          </div>
        </div>
      </div>
    </div>

    <!-- Input -->
    <form data-test="chat-form" class="flex gap-3 items-end group" @submit.prevent="send">
      <div class="relative flex-1 transition-all duration-300">
        <div class="absolute -inset-0.5 bg-gradient-to-r from-primary-500/20 to-purple-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition duration-500 pointer-events-none"></div>
        <textarea
            data-test="chat-input"
            v-model="input"
            rows="1"
            placeholder="Ask about the repository..."
            class="relative w-full min-h-14 resize-none rounded-2xl border border-neutral-800/60 bg-neutral-900/80 backdrop-blur-sm px-5 py-4 text-sm text-neutral-100 placeholder-neutral-500 focus:outline-none focus:ring-1 focus:ring-primary-500/50 shadow-inner"
            :disabled="loading || !repo"
            @keydown.enter.exact.prevent="send"
            @keydown.enter.shift.exact.stop
        />
      </div>
      <UButton 
        :disabled="loading || !trimmedInput" 
        type="submit" 
        data-test="send-button"
        color="primary"
        variant="solid"
        class="h-14 px-6 rounded-2xl shadow-lg shadow-primary-500/20 transition-all hover:shadow-primary-500/40"
      >
        <template #trailing>
          <UIcon name="lucide:send" class="w-4 h-4 ml-1" />
        </template>
        Send
      </UButton>
    </form>

  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import ChatMessage from '@/components/ChatMessage.vue'
import { askRepo } from '@/composables/api'
import { buildBlocks } from '@/utils/chatParser'
import type {ChatMessageType} from "~/types/api";

const props = defineProps<{ repo: string; model?: string }>()

const input = ref('')
const loading = ref(false)
const messages = ref<ChatMessageType[]>([])
const messagesContainer = ref<HTMLElement | null>(null)

const trimmedInput = computed(() => input.value.trim())

async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

async function send() {
  if (!trimmedInput.value || loading.value || !props.repo) return

  const question = trimmedInput.value
  input.value = ''

  messages.value.push({
    id: Date.now(),
    role: 'user',
    text: question
  })

  await scrollToBottom()
  loading.value = true

  try {
    const res = await askRepo(props.repo, question, props.model)
    const blocks = await buildBlocks(res.answer)

    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      text: res.answer,
      blocks,
      sources: res.sources ?? [],
      languages: res.languages ?? [],
      framework: res.framework ?? null,
      entrypoints: res.entrypoints ?? []
    })
  } catch {
    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      text: 'Something went wrong.'
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

watch(() => props.repo, () => {
  messages.value = []
  input.value = ''
})
</script>