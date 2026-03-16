const API = "http://localhost:8000"

export const getRepos = () => {
    return $fetch(`${API}/repos`)
}

export const askRepo = async (repo: string, question: string, model?: string) => {
    return await $fetch(`${API}/query/ask`, {
        method: "POST",
        body: {
            repo,
            question,
            model
        }
    })
}

export const getModels = () => {
    return $fetch(`${API}/models`)
}