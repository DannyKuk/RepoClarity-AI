import ChatMessage from '@/components/ChatMessage.vue'
import {mountWithStubs} from "~/tests/utils/mount";

describe('ChatMessage', () => {

    it('renders user message correctly', () => {
        const wrapper = mountWithStubs(ChatMessage, {
            props: {
                message: {
                    id: 1,
                    role: 'user',
                    text: 'Hello world'
                }
            }
        })

        expect(wrapper.find('[data-test="message-role"]').text()).toBe('You')
        expect(wrapper.find('[data-test="message-text"]').text()).toBe('Hello world')
    })

    it('renders assistant markdown', () => {
        const wrapper = mountWithStubs(ChatMessage, {
            props: {
                message: {
                    id: 1,
                    role: 'assistant',
                    text: '',
                    blocks: [
                        {
                            type: 'markdown',
                            html: '<p>Hello <strong>world</strong></p>'
                        }
                    ]
                }
            }
        })

        const markdown = wrapper.find('[data-test="markdown"]')
        expect(markdown.exists()).toBe(true)
        expect(markdown.html()).toContain('<strong>world</strong>')
    })

    it('renders framework info', () => {
        const wrapper = mountWithStubs(ChatMessage, {
            props: {
                message: {
                    id: 1,
                    role: 'assistant',
                    text: '',
                    blocks: [],
                    framework: 'Vue'
                }
            }
        })

        expect(wrapper.find('[data-test="framework"]').text()).toBe('Vue')
    })

    it('renders sources list', () => {
        const wrapper = mountWithStubs(ChatMessage, {
            props: {
                message: {
                    id: 1,
                    role: 'assistant',
                    text: '',
                    blocks: [],
                    sources: [
                        { path: 'file1.ts', start: 0, end: 10 },
                        { path: 'file2.ts', start: 0, end: 20 }
                    ]
                }
            }
        })

        const sources = wrapper.findAll('[data-test="sources"]')
        expect(sources.length).toBeGreaterThan(0)

        const text = wrapper.text()

        expect(text).toContain('file1.ts')
        expect(text).toContain('file2.ts')
    })

})