import ChatBox from '@/components/ChatBox.vue'
import { vi } from 'vitest'
import { mountWithStubs } from "~/tests/utils/mount";
import flushPromises from 'flush-promises'

vi.mock('@/composables/api', () => ({
    askRepo: vi.fn()
}))

vi.mock('@/utils/chatParser', () => ({
    buildBlocks: vi.fn().mockResolvedValue([
        { type: 'markdown', html: '<p>Parsed</p>' }
    ])
}))

describe('ChatBox', () => {

    function createWrapper() {
        return mountWithStubs(ChatBox, {
            props: {
                repo: 'my-repo'
            },
        })
    }

    it('shows empty state initially', () => {
        const wrapper = createWrapper()

        const empty = wrapper.find('[data-test="empty-state"]')
        expect(empty.exists()).toBe(true)
        expect(empty.text()).toContain('my-repo')
    })

    it('does not send empty input', async () => {
        const { askRepo } = await import('@/composables/api')

        const wrapper = createWrapper()

        await wrapper.find('[data-test="chat-form"]').trigger('submit')

        expect(askRepo).not.toHaveBeenCalled()
    })

    it('adds user message when sending', async () => {
        const wrapper = createWrapper()

        const input = wrapper.find('[data-test="chat-input"]')
        await input.setValue('Hello')

        await wrapper.find('[data-test="chat-form"]').trigger('submit')

        expect(wrapper.text()).toContain('Hello')
    })

    it('calls API and renders assistant response', async () => {
        const { askRepo } = await import('@/composables/api')

        // @ts-ignore
        askRepo.mockResolvedValue({
            answer: 'Answer text',
            sources: ['file.ts'],
            framework: 'Vue',
            entrypoints: []
        })

        const wrapper = createWrapper()

        await wrapper.find('[data-test="chat-input"]').setValue('Question')
        await wrapper.find('[data-test="chat-form"]').trigger('submit')

        await flushPromises()
        await Promise.resolve()

        const messages = wrapper.findAll('[data-test="message"]')

        expect(messages.length).toBeGreaterThan(1)
    })

    it('shows loading state while waiting', async () => {
        const { askRepo } = await import('@/composables/api')

        // @ts-ignore
        askRepo.mockImplementation(() => new Promise(() => {})) // never resolves

        const wrapper = createWrapper()

        await wrapper.find('[data-test="chat-input"]').setValue('Test')
        await wrapper.find('[data-test="chat-form"]').trigger('submit')

        await flushPromises()

        expect(wrapper.find('[data-test="loading"]').exists()).toBe(true)
    })

    it('handles API error', async () => {
        const { askRepo } = await import('@/composables/api')

        // @ts-ignore
        askRepo.mockRejectedValue(new Error('fail'))

        const wrapper = createWrapper()

        await wrapper.find('[data-test="chat-input"]').setValue('Test')
        await wrapper.find('[data-test="chat-form"]').trigger('submit')

        await flushPromises()
        await Promise.resolve()

        const messages = wrapper.findAll('[data-test="message"]')
        const lastMessage = messages[messages.length - 1]

        expect(lastMessage?.text()).toContain('Something went wrong.')
    })

    it('clears messages when repo changes', async () => {
        const wrapper = createWrapper()

        await wrapper.find('[data-test="chat-input"]').setValue('Hello')
        await wrapper.find('[data-test="chat-form"]').trigger('submit')

        expect(wrapper.text()).toContain('Hello')

        await wrapper.setProps({ repo: 'new-repo' })
        await flushPromises()

        expect(wrapper.text()).not.toContain('Hello')
    })

})