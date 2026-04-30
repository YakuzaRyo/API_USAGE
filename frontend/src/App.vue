<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { LayoutDashboard, Server, FolderOpen, Sparkles, ChevronLeft, ChevronRight } from 'lucide-vue-next'

const route = useRoute()

const collapsed = ref(
  (() => { try { return localStorage.getItem('sidebar-collapsed') === 'true' } catch { return false } })()
)
watch(collapsed, v => {
  try { localStorage.setItem('sidebar-collapsed', String(v)) } catch {}
})

function toggleSidebar() {
  collapsed.value = !collapsed.value
}

function onSidebarTransitionEnd() {
  window.dispatchEvent(new Event('resize'))
}

const navItems = [
  { path: '/dashboard', label: '用量看板', icon: LayoutDashboard },
  { path: '/providers', label: '厂商管理', icon: Server },
  { path: '/categories', label: '分类管理', icon: FolderOpen },
]

const toggleIcon = computed(() => collapsed.value ? ChevronRight : ChevronLeft)
</script>

<template>
  <aside
    class="sidebar"
    :class="{ collapsed }"
    @transitionend="onSidebarTransitionEnd"
  >
    <h1 class="sidebar-brand">{{ collapsed ? 'L' : 'LLM Usage' }}</h1>
    <nav class="sidebar-nav">
      <RouterLink
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="sidebar-link"
        :class="{ active: route.path === item.path }"
        :title="collapsed ? item.label : undefined"
      >
        <component :is="item.icon" :size="18" class="sidebar-icon" />
        <span class="sidebar-link-text">{{ item.label }}</span>
      </RouterLink>
    </nav>
    <button class="toggle-btn" @click="toggleSidebar" :title="collapsed ? '展开侧边栏' : '收起侧边栏'">
      <component :is="toggleIcon" :size="14" />
    </button>
  </aside>
  <main class="main-content">
    <div class="main-inner">
      <RouterView />
    </div>
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
  position: relative;
  overflow: visible;
  transition: width 0.15s ease;
}

.sidebar.collapsed {
  width: 52px;
  padding: var(--space-md) var(--space-xs);
}

.sidebar-brand {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.5px;
  white-space: nowrap;
  text-align: center;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  text-decoration: none;
  color: var(--color-text-muted);
  font-weight: 600;
  font-size: 14px;
  border: var(--border-width) solid transparent;
  transition: color 0.15s, border-color 0.15s, background 0.15s, box-shadow 0.15s, transform 0.15s;
  white-space: nowrap;
}

.sidebar-icon {
  flex-shrink: 0;
}

.sidebar-link-text {
  overflow: hidden;
  transition: opacity 0.15s;
}

.collapsed .sidebar-link-text {
  opacity: 0;
  width: 0;
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

.collapsed .sidebar-link {
  justify-content: center;
  padding: var(--space-sm);
}

.collapsed .sidebar-brand {
  text-align: center;
}

.toggle-btn {
  position: absolute;
  top: 50%;
  right: 4px;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  background: var(--color-surface);
  border: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
  opacity: 0;
  transition: opacity 0.15s, transform 0.1s, box-shadow 0.1s, right 0.15s ease;
  cursor: pointer;
  z-index: 10;
}

.collapsed .toggle-btn {
  right: -28px;
}

.sidebar:hover .toggle-btn {
  opacity: 1;
}

.toggle-btn:hover {
  transform: translateY(-50%) translate(-1px, -1px);
  box-shadow: var(--shadow-hover);
}

.toggle-btn:active {
  transform: translateY(-50%) translate(1px, 1px);
  box-shadow: none;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  height: 100vh;
}

.main-inner {
  padding: var(--space-xl);
}
</style>
