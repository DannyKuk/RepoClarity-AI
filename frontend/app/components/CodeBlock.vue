<template>
  <div class="relative my-3 rounded-lg border border-neutral-700 bg-neutral-950 overflow-hidden">
    <!-- Header -->
    <div class="flex items-center justify-between px-4 py-2 text-xs border-b border-neutral-800 bg-neutral-900">
      <span class="uppercase text-neutral-400 font-medium tracking-wide">
        {{ language || 'code' }}
      </span>

      <button
          class="text-neutral-400 hover:text-white transition-colors duration-150"
          @click="copy"
      >
        {{ copied ? 'Copied!' : 'Copy' }}
      </button>
    </div>

    <!-- Code container -->
    <div class="overflow-auto max-h-96 scrollbar-thin scrollbar-track-neutral-900 scrollbar-thumb-neutral-700 hover:scrollbar-thumb-neutral-600">
      <pre class="m-0 p-0">
        <code
            ref="codeEl"
            class="block text-sm leading-6 whitespace-pre px-4 py-4 min-w-full"
        ></code>
      </pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

const props = defineProps<{
  code: string
  language?: string
}>()

const codeEl = ref<HTMLElement | null>(null)
const copied = ref(false)

function copy() {
  navigator.clipboard.writeText(props.code.trim())
  copied.value = true
  setTimeout(() => (copied.value = false), 1800)
}

onMounted(() => {
  if (!codeEl.value) return

  let result

  if (props.language && hljs.getLanguage(props.language)) {
    result = hljs.highlight(props.code, { language: props.language })
  } else {
    result = hljs.highlightAuto(props.code)
  }

  codeEl.value.innerHTML = result.value
})
</script>