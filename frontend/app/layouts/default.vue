<template>
  <div class="min-h-screen bg-transparent text-neutral-100 flex relative overflow-hidden">
    <!-- Animated background accents -->
    <div class="absolute top-0 right-0 w-[500px] h-[500px] bg-primary-900/20 blur-[100px] rounded-full pointer-events-none -z-10 animate-pulse" style="animation-duration: 4s;"></div>
    <div class="absolute bottom-0 left-0 w-[600px] h-[600px] bg-purple-900/10 blur-[120px] rounded-full pointer-events-none -z-10"></div>

    <aside class="w-80 border-r border-neutral-800/50 bg-neutral-950/40 backdrop-blur-xl p-5 shadow-2xl flex flex-col z-10 transition-all duration-300">
      <div class="flex items-center gap-3 mb-8">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center shadow-lg shadow-primary-500/20">
          <UIcon name="lucide:bot" class="text-white w-5 h-5" />
        </div>
        <h1 class="text-xl font-bold bg-gradient-to-r from-neutral-100 to-neutral-400 bg-clip-text text-transparent tracking-tight">RepoClarity</h1>
      </div>
      <RepoSelector />
    </aside>

    <main class="flex-1 p-8 relative z-10 overflow-y-auto">
      <slot />
    </main>
  </div>
</template>