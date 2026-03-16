<template>
  <div class="min-h-screen bg-neutral-950 text-neutral-100 flex">
    <aside class="w-72 border-r border-neutral-800 p-4">
      <RepoSelector />
    </aside>

    <main class="flex-1 p-6">
      <slot />
    </main>
  </div>
</template>