export interface AskResponse {
    answer: string
    sources: string[]
    framework: string | null
    entrypoints: string[]
}

export interface ModelsResponse {
    models: string[]
}

export interface Repo {
    name: string
    path: string
}