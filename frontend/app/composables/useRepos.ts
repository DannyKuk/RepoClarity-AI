import type { Repo } from "~/types/api"
import { getRepos } from "~/composables/api"

export function useRepos() {
    const repos = ref<Repo[]>([])
    const loading = ref(false)
    const errorVisible = ref(false)

    async function fetchRepos() {
        repos.value = await getRepos()
    }

    async function addRepo(name: string, path: string) {
        const config = useRuntimeConfig()

        loading.value = true
        errorVisible.value = false

        try {
            await $fetch(`${config.public.apiBase}/repos/index`, {
                method: 'POST',
                body: { name, path }
            })

            await fetchRepos()
            return true
        } catch (err) {
            console.error('Failed to index repo', err)
            errorVisible.value = true
            return false
        } finally {
            loading.value = false
        }
    }

    return {
        repos,
        loading,
        errorVisible,
        fetchRepos,
        addRepo
    }
}