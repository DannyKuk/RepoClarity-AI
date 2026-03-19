import ModelSelector from '@/components/ModelSelector.vue'
import { vi } from 'vitest'
import { ref } from 'vue'
import { mountWithStubs } from '~/tests/utils/mount'
import { useModelsStore } from '@/stores/models'


vi.mock('@/stores/models', () => ({
    useModelsStore: vi.fn()
}))

vi.mock('pinia', async (orig) => {
    const actual = await orig()
    return {
        // @ts-ignore
        ...actual,
        storeToRefs: (store: any) => store
    }
})

describe('ModelSelector', () => {

    function createStoreMock() {
        return {
            models: ref(['gpt-4', 'gpt-3.5']),
            loading: ref(false),
            reloadModels: vi.fn()
        }
    }

    function createWrapper(storeMock: any) {
        ;(useModelsStore as any).mockReturnValue(storeMock)

        return mountWithStubs(ModelSelector, {
            props: {
                model: 'gpt-4'
            }
        })
    }

    it('emits model update when selecting', async () => {
        const store = createStoreMock()
        const wrapper = createWrapper(store)

        const select = wrapper.find('select')
        await select.setValue('gpt-3.5')

        const emitted = wrapper.emitted('update:modelValue')
        expect(emitted![0]![0]).toBe('gpt-3.5')
    })

    it('calls reloadModels when button clicked', async () => {
        const store = createStoreMock()
        const wrapper = createWrapper(store)

        await wrapper.find('button').trigger('click')

        expect(store.reloadModels).toHaveBeenCalled()
    })

    it('passes loading state to button', () => {
        const store = createStoreMock()
        store.loading.value = true

        const wrapper = createWrapper(store)

        const button = wrapper.find('button')
        expect(button.attributes()).toHaveProperty('disabled')
    })

})