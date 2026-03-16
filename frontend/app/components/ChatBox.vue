<template>
  <div class="space-y-4">

    <div
        v-for="msg in messages"
        :key="msg.id"
        class="p-3 rounded bg-neutral-900"
    >
      <p class="text-sm text-neutral-400 mb-1">
        {{ msg.role }}
      </p>

      <p>{{ msg.text }}</p>
    </div>

    <form @submit.prevent="send">
      <input
          v-model="input"
          placeholder="Ask about the repository..."
          class="w-full p-3 bg-neutral-900 border border-neutral-800 rounded"
      />
    </form>

  </div>
</template>

<script setup lang="ts">
import { askRepo } from "~/composables/api";

const props = defineProps<{
  repo: string
  model?: string
}>()

const input = ref("")
const messages = ref<any[]>([])

const send = async () => {
  if (!input.value) return

  const question = input.value
  input.value = ""

  messages.value.push({
    id: Date.now(),
    role: "You",
    text: question
  })

  const res = await askRepo(props.repo, question, props.model)

  messages.value.push({
    id: Date.now() + 1,
    role: "RepoMind",
    text: res.answer
  })
}
</script>