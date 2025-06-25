import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 模态框状态
  const isModalOpen = ref(false)
  const modalComponent = ref(null)
  const modalProps = ref({})

  // 消息状态
  const messages = ref([])
  let messageId = 0

  // 模态框方法
  const openModal = (component, props = {}) => {
    modalComponent.value = component
    modalProps.value = props
    isModalOpen.value = true
  }

  const closeModal = () => {
    isModalOpen.value = false
    modalComponent.value = null
    modalProps.value = {}
  }

  // 消息方法
  const showMessage = (text, type = 'success') => {
    const message = {
      id: ++messageId,
      text,
      type
    }
    messages.value.push(message)
    
    setTimeout(() => {
      removeMessage(message.id)
    }, 3000)
  }

  const removeMessage = (id) => {
    const index = messages.value.findIndex(m => m.id === id)
    if (index > -1) {
      messages.value.splice(index, 1)
    }
  }

  return {
    isModalOpen,
    modalComponent,
    modalProps,
    messages,
    openModal,
    closeModal,
    showMessage,
    removeMessage
  }
})
