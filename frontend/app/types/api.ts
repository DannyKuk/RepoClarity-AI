export interface AskResponse {
    answer: string
    sources: string[]
    languages: string[]
    framework: string | null
    entrypoints: string[]
}

export type ChatMessageType = {
    id: number
    role: 'user' | 'assistant'
    text: string
    blocks?: any[]
    sources?: string[]
    languages?: string[]
    framework?: string | null
    entrypoints?: string[]
}

export interface ModelsResponse {
    models: string[]
}

export interface Repo {
    name: string
    path: string
    languages: string | null
}