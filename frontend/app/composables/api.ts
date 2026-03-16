const API = "http://localhost:8000"

export const getRepos = () => {
    return $fetch(`${API}/repos`)
}

export const askRepo = (repo: string, question: string, model?: string) => {
    return $fetch(`${API}/query/ask`, {
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