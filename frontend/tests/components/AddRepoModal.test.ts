import { mount } from '@vue/test-utils'
import AddRepoModal from '@/components/AddRepoModal.vue'
import { nextTick } from 'vue'

describe('AddRepoModal', () => {
    function createWrapper() {
        return mount(AddRepoModal, {
            props: {
                loading: false,
                open: false,
            },
            global: {
                stubs: {
                    UModal: {
                        template: `
              <div>
                <slot />
                <slot name="body" />
              </div>
            `
                    },
                    UButton: {
                        props: ['label', 'loading', 'disabled'],
                        template: `
                          <button
                              :data-label="label"
                              @click="$emit('click')"
                          >
                            {{ label }}
                          </button>
                        `
                    },
                    UInput: {
                        props: ['modelValue'],
                        template: `
                          <input
                              :value="modelValue"
                              @input="$emit('update:modelValue', $event.target.value)"
                          />
                        `
                    }
                }
            }
        })
    }

    it('opens modal when trigger button is clicked', async () => {
        const wrapper = createWrapper()

        const triggerButton = wrapper.find('button:not([data-label])')
        expect(triggerButton.exists()).toBe(true)

        await triggerButton.trigger('click')

        expect(wrapper.emitted('update:open')).toBeTruthy()
    })

    it('emits correct payload on submit', async () => {
        const wrapper = createWrapper()

        const inputs = wrapper.findAll('input')
        expect(inputs).toHaveLength(2)

        const [pathInput, nameInput] = inputs

        await pathInput?.setValue('/some/path')
        await nameInput?.setValue('My Repo')

        const addButton = wrapper.find('button[data-label="Add"]')
        expect(addButton.exists()).toBe(true)

        await addButton.trigger('click')

        const emitted = wrapper.emitted('add')
        expect(emitted).toBeTruthy()
        expect(emitted![0]![0]).toEqual({
            name: 'My Repo',
            path: '/some/path'
        })
    })

    it('does not emit when fields are empty', async () => {
        const wrapper = createWrapper()

        const addButton = wrapper.find('button[data-label="Add"]')
        expect(addButton.exists()).toBe(true)

        await addButton.trigger('click')

        expect(wrapper.emitted('add')).toBeFalsy()
    })

    it('resets inputs when modal opens', async () => {
        const wrapper = createWrapper()

        const inputs = wrapper.findAll('input')
        expect(inputs).toHaveLength(2)

        const [pathInput, nameInput] = inputs

        await pathInput?.setValue('/old/path')
        await nameInput?.setValue('Old Name')

        await wrapper.setProps({ open: true })
        await nextTick()

        expect((pathInput?.element as HTMLInputElement).value).toBe('')
        expect((nameInput?.element as HTMLInputElement).value).toBe('')
    })
})