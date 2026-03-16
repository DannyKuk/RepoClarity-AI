<template>
  <div class="flex h-full flex-col gap-4">

    <!-- Messages -->
    <div
        ref="messagesContainer"
        class="flex-1 space-y-4 overflow-y-auto rounded-xl border border-neutral-800 bg-neutral-950/50 p-4"
    >
      <div
          v-if="messages.length === 0"
          class="flex h-full min-h-75 items-center justify-center text-sm text-neutral-500"
      >
        Ask something about
        <span class="mx-1 font-semibold text-neutral-300">{{ repo }}</span>.
      </div>

      <div
          v-for="message in messages"
          :key="message.id"
          class="flex"
          :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div
            class="max-w-[85%] rounded-2xl border px-4 py-3 shadow-sm"
            :class="
            message.role === 'user'
              ? 'border-neutral-700 bg-neutral-800 text-neutral-100'
              : 'border-neutral-800 bg-neutral-900 text-neutral-100'
          "
        >
          <div class="mb-2 text-xs font-medium uppercase tracking-wide text-neutral-400">
            {{ message.role === 'user' ? 'You' : 'RepoClarity' }}
          </div>

          <!-- User -->
          <div
              v-if="message.role === 'user'"
              class="whitespace-pre-wrap wrap-break-word text-sm leading-6"
          >
            {{ message.text }}
          </div>

          <!-- Assistant -->
          <div v-else class="space-y-4">

            <template v-for="(block, i) in message.blocks" :key="i">

              <!-- Markdown -->
              <div
                  v-if="block.type === 'markdown'"
                  class="prose prose-invert max-w-none"
                  v-html="block.html"
              />

              <!-- Code -->
              <CodeBlock
                  v-else
                  :code="block.code"
                  :language="block.lang"
              />

            </template>

            <!-- Framework -->
            <div
                v-if="message.framework || (message.entrypoints && message.entrypoints.length)"
                class="rounded-lg border border-neutral-800 bg-neutral-950/70 p-3 text-xs text-neutral-300"
            >
              <div v-if="message.framework" class="mb-2">
                <span class="font-semibold text-neutral-200">Framework:</span>
                {{ message.framework }}
              </div>

              <div v-if="message.entrypoints?.length">
                <div class="mb-1 font-semibold text-neutral-200">Entrypoints</div>
                <ul class="space-y-1">
                  <li
                      v-for="entrypoint in message.entrypoints"
                      :key="entrypoint"
                      class="break-all text-neutral-400"
                  >
                    {{ entrypoint }}
                  </li>
                </ul>
              </div>
            </div>

            <!-- Sources -->
            <div
                v-if="message.sources?.length"
                class="rounded-lg border border-neutral-800 bg-neutral-950/70 p-3 text-xs"
            >
              <div class="mb-2 font-semibold text-neutral-200">Sources</div>
              <ul class="space-y-1">
                <li
                    v-for="source in message.sources"
                    :key="source"
                    class="break-all text-neutral-400"
                >
                  {{ source }}
                </li>
              </ul>
            </div>

          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-start">
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
    <form class="flex gap-2" @submit.prevent="send">
      <textarea
          v-model="input"
          rows="1"
          placeholder="Ask about the repository..."
          class="min-h-13 flex-1 resize-none rounded-xl border border-neutral-800 bg-neutral-900 px-4 py-3 text-sm text-neutral-100 outline-none transition focus:border-neutral-600"
          :disabled="loading || !repo"
          @keydown.enter.exact.prevent="send"
          @keydown.enter.shift.exact.stop
      />

      <button
          type="submit"
          class="rounded-xl border border-neutral-700 bg-neutral-100 px-4 py-2 text-sm font-medium text-neutral-900 transition hover:bg-white disabled:cursor-not-allowed disabled:opacity-50"
          :disabled="loading || !trimmedInput"
      >
        Send
      </button>
    </form>

  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from "vue"
import { marked } from "marked"
import DOMPurify from "dompurify"
import CodeBlock from "~/components/CodeBlock.vue"
import { askRepo } from "~/composables/api"

type MarkdownBlock = {
  type: "markdown"
  html: string
}

type CodeBlockType = {
  type: "code"
  code: string
  lang: string
}

type Block = MarkdownBlock | CodeBlockType

type ChatMessage = {
  id: number
  role: "user" | "assistant"
  text: string
  blocks?: Block[]
  sources?: string[]
  framework?: string | null
  entrypoints?: string[]
}

const props = defineProps<{ repo: string; model?: string }>()

const input = ref("")
const loading = ref(false)
const messages = ref<ChatMessage[]>([])
const messagesContainer = ref<HTMLElement | null>(null)

const trimmedInput = computed(() => input.value.trim())

function parseBlocks(text: string): { type: "markdown"; content: string } | any {
  const blocks: any[] = []
  const regex = /```(\w+)?\n([\s\S]*?)```/g

  let lastIndex = 0
  let match: RegExpExecArray | null

  while ((match = regex.exec(text))) {
    if (match.index > lastIndex) {
      blocks.push({
        type: "markdown",
        content: text.slice(lastIndex, match.index)
      })
    }

    const [, lang, code] = match

    blocks.push({
      type: "code",
      lang: lang ?? "text",
      code: code
    })

    lastIndex = match.index + match[0].length
  }

  if (lastIndex < text.length) {
    blocks.push({
      type: "markdown",
      content: text.slice(lastIndex)
    })
  }

  return blocks
}

async function renderMarkdown(text: string): Promise<string> {
  const html = await marked.parse(text)
  return DOMPurify.sanitize(html)
}

async function buildBlocks(text: string): Promise<Block[]> {
  const parsed = parseBlocks(text)
  const result: Block[] = []

  for (const block of parsed) {
    if (block.type === "markdown") {
      result.push({
        type: "markdown",
        html: await renderMarkdown(block.content)
      })
    } else {
      result.push({
        type: "code",
        code: block.code,
        lang: block.lang
      })
    }
  }

  return result
}

async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

async function send() {
  if (!trimmedInput.value || loading.value || !props.repo) return

  const question = trimmedInput.value
  input.value = ""

  messages.value.push({
    id: Date.now(),
    role: "user",
    text: question
  })

  await scrollToBottom()
  loading.value = true

  try {
    const res = await askRepo(props.repo, question, props.model)

    const blocks = await buildBlocks(res.answer)

    messages.value.push({
      id: Date.now() + 1,
      role: "assistant",
      text: res.answer,
      blocks,
      sources: res.sources ?? [],
      framework: res.framework ?? null,
      entrypoints: res.entrypoints ?? []
    })

  } catch {
    messages.value.push({
      id: Date.now() + 1,
      role: "assistant",
      text: "Something went wrong."
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

watch(() => props.repo, () => {
  messages.value = []
  input.value = ""
})
</script>