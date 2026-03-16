<template>
  <select
      v-model="model"
      class="border border-neutral-700 bg-neutral-900 p-2 rounded mb-4"
  >
    <option
        v-for="m in models"
        :key="m"
        :value="m"
    >
      {{ m }}
    </option>
  </select>
</template>

<script setup lang="ts">
import { getModels } from "~/composables/api";

const model = defineModel<string>()

const models = ref<string[]>([])

onMounted(async () => {
  const res = await getModels()
  models.value = res.models
})
</script>