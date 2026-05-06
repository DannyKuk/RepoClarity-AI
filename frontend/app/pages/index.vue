<template>
  <div class="flex flex-col justify-center items-center h-full">
    <div class="relative group">
      <div class="absolute -inset-1 bg-gradient-to-r from-primary-500 to-purple-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
      <div class="relative bg-neutral-950/80 backdrop-blur-xl ring-1 ring-neutral-800 p-8 rounded-2xl flex flex-col items-center">
        <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500/20 to-purple-600/20 border border-primary-500/30 flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(59,130,246,0.3)]">
          <UIcon name="lucide:sparkles" class="w-8 h-8 text-primary-400" />
        </div>
        <h2 class="text-2xl font-semibold mb-2 bg-gradient-to-r from-neutral-100 to-neutral-300 bg-clip-text text-transparent">Welcome to RepoClarity</h2>
        <p class="text-neutral-400 text-center max-w-sm">
          Select a repository from the sidebar to start asking questions and exploring your codebase.
        </p>
      </div>
    </div>
  </div>
</template>