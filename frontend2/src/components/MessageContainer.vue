<template>
  <div class="message-container">
    <div
      v-for="message in appStore.messages"
      :key="message.id"
      class="message"
      :class="[`message-${message.type}`]"
    >
      <i class="message-icon" :class="getMessageIcon(message.type)"></i>
      <span class="message-text">{{ message.text }}</span>
      <button class="message-close" @click="appStore.removeMessage(message.id)">
        <i class="fas fa-times"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

const getMessageIcon = (type) => {
  const iconMap = {
    success: 'fas fa-check-circle',
    error: 'fas fa-exclamation-circle',
    warning: 'fas fa-exclamation-triangle',
    info: 'fas fa-info-circle'
  }
  return iconMap[type] || iconMap.info
}
</script>

<style scoped>
.message-container {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  pointer-events: none;
}

.message {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 300px;
  max-width: 400px;
  pointer-events: auto;
  animation: messageSlideIn 0.3s ease-out;
  border-left: 4px solid;
}

.message-success {
  border-left-color: var(--success-color);
  background: linear-gradient(145deg, #f0fff4, #e6fffa);
}

.message-error {
  border-left-color: var(--danger-color);
  background: linear-gradient(145deg, #fff5f5, #fed7d7);
}

.message-warning {
  border-left-color: var(--warning-color);
  background: linear-gradient(145deg, #fffbeb, #fef3c9);
}

.message-info {
  border-left-color: var(--info-color);
  background: linear-gradient(145deg, #ebf8ff, #bee3f8);
}

.message-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.message-success .message-icon {
  color: var(--success-color);
}

.message-error .message-icon {
  color: var(--danger-color);
}

.message-warning .message-icon {
  color: var(--warning-color);
}

.message-info .message-icon {
  color: var(--info-color);
}

.message-text {
  flex: 1;
  color: var(--gray-800);
  font-weight: 500;
}

.message-close {
  background: none;
  border: none;
  color: var(--gray-500);
  cursor: pointer;
  font-size: 1rem;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.message-close:hover {
  background: rgba(0, 0, 0, 0.1);
  color: var(--gray-700);
}

@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
