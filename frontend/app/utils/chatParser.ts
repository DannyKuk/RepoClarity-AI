import { marked } from 'marked'
import DOMPurify from 'dompurify'

export function parseBlocks(text: string) {
    const blocks: any[] = []
    const regex = /```(\w+)?\n([\s\S]*?)```/g

    let lastIndex = 0
    let match: RegExpExecArray | null

    while ((match = regex.exec(text))) {
        if (match.index > lastIndex) {
            blocks.push({
                type: 'markdown',
                content: text.slice(lastIndex, match.index)
            })
        }

        const [, lang, code] = match

        blocks.push({
            type: 'code',
            lang: lang ?? 'text',
            code
        })

        lastIndex = match.index + match[0].length
    }

    if (lastIndex < text.length) {
        blocks.push({
            type: 'markdown',
            content: text.slice(lastIndex)
        })
    }

    return blocks
}

export async function renderMarkdown(text: string) {
    const html = await marked.parse(text)
    return DOMPurify.sanitize(html)
}

export async function buildBlocks(text: string) {
    const parsed = parseBlocks(text)
    const result: any[] = []

    for (const block of parsed) {
        if (block.type === 'markdown') {
            result.push({
                type: 'markdown',
                html: await renderMarkdown(block.content)
            })
        } else {
            result.push(block)
        }
    }

    return result
}