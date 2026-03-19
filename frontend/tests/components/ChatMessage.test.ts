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
                    sources: ['file1.ts', 'file2.ts']
                }
            }
        })

        const sources = wrapper.find('[data-test="sources"]')
        expect(sources.exists()).toBe(true)
        expect(sources.text()).toContain('file1.ts')
        expect(sources.text()).toContain('file2.ts')
    })

})