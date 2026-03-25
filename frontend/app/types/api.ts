export interface AskResponse {
    answer: string
    sources: Source[]
    languages: string[]
    framework: string | null
    entrypoints: string[]
}

export interface Source {
    path: string
    start?: number
    end?: number
}

export type ChatMessageType = {
    id: number
    role: 'user' | 'assistant'
    text: string
    blocks?: any[]
    sources?: Source[]
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
    languages: string[] | null
}