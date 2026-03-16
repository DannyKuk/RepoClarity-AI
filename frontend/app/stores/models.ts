import type {Ref} from 'vue'

interface Model {
    id: string
    name: string
}

export const useModelsStore = defineStore('models', () => {
    // State
    const models: Ref<Model[]> = ref([])
    const loaded = ref(false)
    const loading = ref(false)
    const error = ref<string | null>(null)

    // Getters (optional but very useful)
    const isEmpty = computed(() => models.value.length === 0)
    const modelById = (id: string) =>
        computed(() => models.value.find(m => m.id === id) ?? null)

    // Actions
    async function fetchModels(force = false) {
        if (loaded.value && !force) return

        loading.value = true
        error.value = null

        try {
            models.value = await $fetch<Model[]>('/api/models')
            loaded.value = true
        } catch (err) {
            console.error('Failed to fetch models:', err)
            error.value = err instanceof Error ? err.message : 'Unknown error'
            // Optional: models.value = []   // ← clear on error?
        } finally {
            loading.value = false
        }
    }

    async function reloadModels() {
        await fetchModels(true)
    }

    function reset() {
        models.value = []
        loaded.value = false
        loading.value = false
        error.value = null
    }

    return {
        // state
        models,
        loaded,
        loading,
        error,

        // getters
        isEmpty,
        modelById,

        // actions
        fetchModels,
        reloadModels,
        reset,
    }
})