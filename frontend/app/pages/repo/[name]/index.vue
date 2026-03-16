<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">
      {{ repoName }}
    </h2>

    <ModelSelector v-model="model" />

    <ChatBox
        :repo="repoName"
        :model="model"
    />
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const repoName = route.params.name as string

const model = ref<string | undefined>()
</script>