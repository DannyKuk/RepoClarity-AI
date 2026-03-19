import RepoItem from '@/components/RepoItem.vue'
import { mountWithStubs } from '~/tests/utils/mount'

describe('RepoItem', () => {

    function createRepo(overrides = {}) {
        return {
            name: 'my-repo',
            framework: 'Vue',
            ...overrides
        }
    }

    function createWrapper(repo: any) {
        return mountWithStubs(RepoItem, {
            props: { repo }
        })
    }

    it('renders repo name', () => {
        const wrapper = createWrapper(createRepo())

        expect(wrapper.text()).toContain('my-repo')
    })

    it('renders framework badge when present', () => {
        const wrapper = createWrapper(createRepo({ framework: 'Vue' }))

        const badge = wrapper.find('[data-test="badge"]')
        expect(badge.exists()).toBe(true)
        expect(badge.text()).toBe('Vue')
    })

    it('does not render badge when framework is missing', () => {
        const wrapper = createWrapper(createRepo({ framework: null }))

        expect(wrapper.find('[data-test="badge"]').exists()).toBe(false)
    })

    it('emits settings event when button is clicked', async () => {
        const repo = createRepo()
        const wrapper = createWrapper(repo)

        const button = wrapper.find('button')
        await button.trigger('click')

        const emitted = wrapper.emitted('settings')
        expect(emitted).toBeTruthy()
        expect(emitted![0]![0]).toEqual(repo)
    })

    it('renders correct link', () => {
        const wrapper = createWrapper(createRepo({ name: 'test-repo' }))

        const link = wrapper.find('a')
        expect(link.attributes('href')).toBe('/repo/test-repo')
    })

})