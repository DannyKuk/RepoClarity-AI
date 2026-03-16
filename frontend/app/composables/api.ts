import type {AskResponse, ModelsResponse, Repo} from "~/types/api";

const API = "http://localhost:8000"

export const getRepos = async (): Promise<Repo[]> => {
    return $fetch<Repo[]>(`${API}/repos`)
}

export const askRepo = async (
    repo: string,
    question: string,
    model?: string
): Promise<AskResponse> => {
    return $fetch<AskResponse>(`${API}/query/ask`, {
        method: "POST",
        body: {
            repo,
            question,
            model
        }
    })
}

export const getModels = async (): Promise<ModelsResponse> => {
    return $fetch<ModelsResponse>(`${API}/models`)
}