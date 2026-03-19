import AddRepoModal from '@/components/AddRepoModal.vue'
import { nextTick } from 'vue'
import {mountWithStubs} from "~/tests/utils/mount";

describe('AddRepoModal', () => {
    function createWrapper() {
        return mountWithStubs(AddRepoModal, {
            props: {
                loading: false,
                open: false,
            },
        })
    }

    it('opens modal when trigger button is clicked', async () => {
        const wrapper = createWrapper()

        const openButton = wrapper.find('[data-test="open-button"]')
        expect(openButton.exists()).toBe(true)

        await openButton.trigger('click')

        expect(wrapper.emitted('update:open')).toBeTruthy()
    })

    it('emits correct payload on submit', async () => {
        const wrapper = createWrapper()

        const pathInput = wrapper.find('[data-test="input-path"]')
        const nameInput = wrapper.find('[data-test="input-name"]')

        expect(pathInput.exists()).toBe(true)
        expect(nameInput.exists()).toBe(true)

        await pathInput.setValue('/some/path')
        await nameInput.setValue('My Repo')

        const addButton = wrapper.find('[data-test="add-button"]')
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

        const addButton = wrapper.find('[data-test="add-button"]')
        expect(addButton.exists()).toBe(true)

        await addButton.trigger('click')

        expect(wrapper.emitted('add')).toBeFalsy()
    })

    it('resets inputs when modal opens', async () => {
        const wrapper = createWrapper()

        const pathInput = wrapper.find('[data-test="input-path"]')
        const nameInput = wrapper.find('[data-test="input-name"]')

        await pathInput.setValue('/old/path')
        await nameInput.setValue('Old Name')

        await wrapper.setProps({ open: true })
        await nextTick()

        expect((pathInput.element as HTMLInputElement).value).toBe('')
        expect((nameInput.element as HTMLInputElement).value).toBe('')
    })
})