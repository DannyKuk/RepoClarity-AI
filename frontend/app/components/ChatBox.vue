<template>
  <div class="flex h-full flex-col gap-4">

    <!-- Messages -->
    <div
        ref="messagesContainer"
        data-test="messages-container"
        class="flex-1 space-y-4 overflow-y-auto rounded-xl border border-neutral-800 bg-neutral-950/50 p-4"
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
        <div class="max-w-[85%] rounded-2xl border border-neutral-800 bg-neutral-900 px-4 py-3">
          <div class="mb-2 text-xs font-medium uppercase tracking-wide text-neutral-400">
            RepoClarity
          </div>
          <div class="flex items-center gap-2 text-sm text-neutral-400">
            <span class="h-2 w-2 animate-pulse rounded-full bg-neutral-500"/>
            Thinking...
          </div>
        </div>
      </div>
    </div>

    <!-- Input -->
    <form data-test="chat-form" class="flex gap-2" @submit.prevent="send">
      <textarea
          data-test="chat-input"
          v-model="input"
          rows="1"
          placeholder="Ask about the repository..."
          class="min-h-13 flex-1 resize-none rounded-xl border border-neutral-800 bg-neutral-900 px-4 py-3 text-sm text-neutral-100"
          :disabled="loading || !repo"
          @keydown.enter.exact.prevent="send"
          @keydown.enter.shift.exact.stop
      />

      <button
          data-test="send-button"
          type="submit"
          :disabled="loading || !trimmedInput"
      >
        Send
      </button>
    </form>

  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import ChatMessage from '~/components/ChatMessage.vue'
import { askRepo } from '~/composables/api'
import { buildBlocks } from '~/utils/chatParser'

type ChatMessageType = {
  id: number
  role: 'user' | 'assistant'
  text: string
  blocks?: any[]
  sources?: string[]
  framework?: string | null
  entrypoints?: string[]
}

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