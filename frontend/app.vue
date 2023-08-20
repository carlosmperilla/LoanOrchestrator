<template>
  <div>
    <ClientOnly>
      <notifications position="top middle" />
    </ClientOnly>
    <NuxtLayout>
      <NuxtLoadingIndicator :throttle="0" />
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup></script>

<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
  filter: blur(2px);
}
</style>
