import { mount } from '@vue/test-utils'

export function mountWithStubs(component: any, options: any = {}) {
    return mount(component, {
        ...options,
        global: {
            ...(options.global || {}),
            stubs: {
                ...(options.global?.stubs || {}),

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
                          :data-test="$attrs['data-test']"
                          :disabled="disabled"
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
                          :data-test="$attrs['data-test']"
                          :value="modelValue"
                          @input="$emit('update:modelValue', $event.target.value)"
                        />
                    `
                },

                USelect: {
                    props: ['modelValue', 'items'],
                    template: `
                        <select
                          :value="modelValue"
                          @change="$emit('update:modelValue', $event.target.value)"
                        >
                          <option v-for="item in items" :key="item" :value="item">
                            {{ item }}
                          </option>
                        </select>
                    `
                },

                NuxtLink: {
                    props: ['to'],
                    template: `<a :href="to"><slot /></a>`
                },

                UBadge: {
                    template: `<span data-test="badge"><slot /></span>`
                },

                USeparator: {
                    template: `<div data-test="separator" />`
                },
            }
        }
    })
}