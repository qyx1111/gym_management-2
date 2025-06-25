const API_BASE_URL = 'http://localhost:5000/api'

class ApiClient {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    }

    try {
      console.log(`API 请求: ${url}`)
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log(`API 响应:`, data)
      return data
    } catch (error) {
      console.error('API request failed:', error)
      
      // 如果是网络错误，返回更友好的错误信息
      if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
        return { 
          success: false, 
          message: '无法连接到服务器，请确保后端服务正在运行',
          error: error
        }
      }
      
      return { 
        success: false, 
        message: error.message || '网络请求失败',
        error: error
      }
    }
  }

  // 会员API
  async getMembers() {
    return this.request('/members')
  }

  async getMember(id) {
    return this.request(`/members/${id}`)
  }

  async searchMembers(term) {
    return this.request(`/members/search?term=${encodeURIComponent(term)}`)
  }

  async createMember(memberData) {
    return this.request('/members', {
      method: 'POST',
      body: JSON.stringify(memberData)
    })
  }

  async updateMember(id, memberData) {
    return this.request(`/members/${id}`, {
      method: 'PUT',
      body: JSON.stringify(memberData)
    })
  }

  async deleteMember(id) {
    return this.request(`/members/${id}`, {
      method: 'DELETE'
    })
  }

  // 教练API
  async getTrainers(activeOnly = false) {
    return this.request(`/trainers?active_only=${activeOnly}`)
  }

  async createTrainer(trainerData) {
    return this.request('/trainers', {
      method: 'POST',
      body: JSON.stringify(trainerData)
    })
  }

  async updateTrainer(id, trainerData) {
    return this.request(`/trainers/${id}`, {
      method: 'PUT',
      body: JSON.stringify(trainerData)
    })
  }

  async deleteTrainer(id) {
    return this.request(`/trainers/${id}`, {
      method: 'DELETE'
    })
  }

  async searchTrainers(term) {
    return this.request(`/trainers/search?term=${encodeURIComponent(term)}`)
  }

  // 课程API
  async getCourses(activeOnly = false) {
    return this.request(`/courses?active_only=${activeOnly}`)
  }

  async searchCourses(term) {
    return this.request(`/courses/search?term=${encodeURIComponent(term)}`)
  }

  async createCourse(courseData) {
    return this.request('/courses', {
      method: 'POST',
      body: JSON.stringify(courseData)
    })
  }

  async updateCourse(id, courseData) {
    return this.request(`/courses/${id}`, {
      method: 'PUT',
      body: JSON.stringify(courseData)
    })
  }

  async deleteCourse(id) {
    return this.request(`/courses/${id}`, {
      method: 'DELETE'
    })
  }

  // 会员卡类型API
  async getCardTypes() {
    return this.request('/card-types')
  }

  async searchCardTypes(term) {
    return this.request(`/card-types/search?term=${encodeURIComponent(term)}`)
  }

  async createCardType(cardTypeData) {
    return this.request('/card-types', {
      method: 'POST',
      body: JSON.stringify(cardTypeData)
    })
  }

  async updateCardType(id, cardTypeData) {
    return this.request(`/card-types/${id}`, {
      method: 'PUT',
      body: JSON.stringify(cardTypeData)
    })
  }

  async deleteCardType(id) {
    return this.request(`/card-types/${id}`, {
      method: 'DELETE'
    })
  }

  // 会员详情API
  async getMemberCards(memberId) {
    return this.request(`/members/${memberId}/cards`)
  }

  async assignCardToMember(memberId, cardData) {
    return this.request(`/members/${memberId}/cards`, {
      method: 'POST',
      body: JSON.stringify(cardData)
    })
  }

  async updateMemberCard(cardId, cardData) {
    return this.request(`/member-cards/${cardId}`, {
      method: 'PUT',
      body: JSON.stringify(cardData)
    })
  }

  async deleteMemberCard(cardId) {
    return this.request(`/member-cards/${cardId}`, {
      method: 'DELETE'
    })
  }

  async getMemberEnrollments(memberId) {
    return this.request(`/members/${memberId}/enrollments`)
  }

  async enrollMemberInCourse(memberId, enrollmentData) {
    return this.request(`/members/${memberId}/enrollments`, {
      method: 'POST',
      body: JSON.stringify(enrollmentData)
    })
  }

  async updateMemberEnrollment(enrollmentId, enrollmentData) {
    return this.request(`/enrollments/${enrollmentId}`, {
      method: 'PUT',
      body: JSON.stringify(enrollmentData)
    })
  }

  async deleteMemberEnrollment(enrollmentId) {
    return this.request(`/enrollments/${enrollmentId}`, {
      method: 'DELETE'
    })
  }

  async getMemberAssignments(memberId) {
    return this.request(`/members/${memberId}/assignments`)
  }

  async assignTrainerToMember(memberId, assignmentData) {
    return this.request(`/members/${memberId}/assignments`, {
      method: 'POST',
      body: JSON.stringify(assignmentData)
    })
  }

  async updateMemberAssignment(assignmentId, assignmentData) {
    return this.request(`/assignments/${assignmentId}`, {
      method: 'PUT',
      body: JSON.stringify(assignmentData)
    })
  }

  async deleteMemberAssignment(assignmentId) {
    return this.request(`/assignments/${assignmentId}`, {
      method: 'DELETE'
    })
  }

  // 教练详情API
  async getTrainerCourses(trainerId) {
    return this.request(`/trainers/${trainerId}/courses`)
  }

  async assignCourseToTrainer(trainerId, assignmentData) {
    return this.request(`/trainers/${trainerId}/courses`, {
      method: 'POST',
      body: JSON.stringify(assignmentData)
    })
  }

  async updateTrainerCourse(assignmentId, assignmentData) {
    return this.request(`/trainer-courses/${assignmentId}`, {
      method: 'PUT',
      body: JSON.stringify(assignmentData)
    })
  }

  async deleteTrainerCourse(assignmentId) {
    return this.request(`/trainer-courses/${assignmentId}`, {
      method: 'DELETE'
    })
  }

  async getTrainerMembers(trainerId) {
    return this.request(`/trainers/${trainerId}/members`)
  }

  async assignMemberToTrainer(trainerId, assignmentData) {
    return this.request(`/trainers/${trainerId}/members`, {
      method: 'POST',
      body: JSON.stringify(assignmentData)
    })
  }

  async updateTrainerMember(assignmentId, assignmentData) {
    return this.request(`/trainer-members/${assignmentId}`, {
      method: 'PUT',
      body: JSON.stringify(assignmentData)
    })
  }

  async deleteTrainerMember(assignmentId) {
    return this.request(`/trainer-members/${assignmentId}`, {
      method: 'DELETE'
    })
  }
}

export const useApi = () => {
  return new ApiClient()
}
