<script setup lang="ts">
import { RouterLink, RouterView, useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { path: '/dashboard', label: '用量看板' },
  { path: '/providers', label: '厂商管理' },
]
</script>

<template>
  <aside class="sidebar">
    <h1 class="sidebar-brand">LLM Usage</h1>
    <nav class="sidebar-nav">
      <RouterLink
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="sidebar-link"
        :class="{ active: route.path === item.path }"
      >
        {{ item.label }}
      </RouterLink>
    </nav>
  </aside>
  <main class="main-content">
    <RouterView />
  </main>
</template>

<style scoped>
.sidebar {
  width: 200px;
  height: 100vh;
  position: sticky;
  top: 0;
  background: var(--color-surface);
  border-right: var(--border-width) solid var(--color-border);
  display: flex;
  flex-direction: column;
  padding: var(--space-lg);
  gap: var(--space-lg);
  flex-shrink: 0;
}

.sidebar-brand {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.sidebar-link {
  padding: var(--space-sm) var(--space-md);
  text-decoration: none;
  color: var(--color-text-muted);
  font-weight: 600;
  font-size: 14px;
  border: var(--border-width) solid transparent;
  transition: color 0.15s, border-color 0.15s, background 0.15s, box-shadow 0.15s, transform 0.15s;
}

.sidebar-link:hover {
  color: var(--color-text);
  background: var(--color-bg);
  transform: translate(-1px, -1px);
  box-shadow: var(--shadow-sm);
}

.sidebar-link.active {
  color: var(--color-text);
  border-left-color: var(--color-primary);
  background: var(--color-bg);
  box-shadow: none;
  transform: none;
}

.main-content {
  flex: 1;
  padding: var(--space-xl);
  max-width: 1200px;
  overflow-y: auto;
  height: 100vh;
}
</style>
