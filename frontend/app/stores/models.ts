export const useModelsStore = defineStore('models', () => {
    const config = useRuntimeConfig()

    const models = ref<string[]>([])
    const loading = ref(false)
    const loaded = ref(false)
    const error = ref<string | null>(null)

    async function fetchModels(force = false) {
        if ((loaded.value && !force) || loading.value) return

        loading.value = true
        error.value = null

        try {
            const res = await $fetch<{ models: string[] }>(
                `${config.public.apiBase}/models`
            )

            models.value = res.models
            loaded.value = true
        } catch (err) {
            console.error(err)
            error.value = 'Failed to fetch models'
        } finally {
            loading.value = false
        }
    }

    async function reloadModels() {
        await fetchModels(true)
    }

    return {
        models,
        loading,
        loaded,
        error,
        fetchModels,
        reloadModels
    }
})