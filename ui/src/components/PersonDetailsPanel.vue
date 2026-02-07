<script setup lang="ts">


interface Person {
    id: string;
    name: string;
    gender: string;
    birth_date?: string;
    death_date?: string;
    biography?: string;
    avatar_url?: string;
}

const props = defineProps<{
  person: Person | null;
  isOpen: boolean;
}>();

const emit = defineEmits(['close']);
</script>

<template>
  <div class="person-details-panel" :class="{ 'open': isOpen }">
    <div class="panel-header">
      <h2>Person Details</h2>
      <button class="close-btn" @click="$emit('close')">&times;</button>
    </div>
    
    <div v-if="person" class="panel-content">
      <div class="avatar-container">
        <img :src="person.avatar_url || 'https://via.placeholder.com/150'" alt="Avatar" class="avatar" />
      </div>
      
      <h3>{{ person.name }}</h3>
      
      <div class="detail-row">
        <strong>Gender:</strong> <span>{{ person.gender }}</span>
      </div>
      
      <div class="detail-row">
        <strong>Birth Date:</strong> <span>{{ person.birth_date || 'Unknown' }}</span>
      </div>
      
      <div class="detail-row">
        <strong>Death Date:</strong> <span>{{ person.death_date || 'N/A' }}</span>
      </div>
      
      <div class="biography-section">
        <strong>Biography:</strong>
        <p>{{ person.biography || 'No biography available.' }}</p>
      </div>
    </div>
    <div v-else class="no-selection">
      <p>Select a person to view details.</p>
    </div>
  </div>
</template>

<style scoped>
.person-details-panel {
  position: absolute;
  top: 0;
  right: -450px; /* Hidden by default */
  width: 400px;
  height: 100%;
  background: var(--color-surface);
  box-shadow: var(--shadow-xl);
  border-left: 1px solid var(--color-border);
  transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 20;
  display: flex;
  flex-direction: column;
}

.person-details-panel.open {
  right: 0;
}

.panel-header {
  padding: var(--spacing-lg);
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h2 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: var(--color-text-secondary);
  cursor: pointer;
  line-height: 1;
  padding: 0;
  transition: color 0.2s;
}

.close-btn:hover {
  color: var(--color-primary);
}

.panel-content {
  padding: var(--spacing-lg);
  overflow-y: auto;
}

.avatar-container {
  display: flex;
  justify-content: center;
  margin-bottom: var(--spacing-lg);
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid var(--color-surface);
  box-shadow: var(--shadow-md);
}

h3 {
  text-align: center;
  margin-top: 0;
  margin-bottom: var(--spacing-lg);
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
}

.detail-row {
  margin-bottom: var(--spacing-md);
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--spacing-sm);
}

.detail-row strong {
  color: var(--color-text-secondary);
}

.detail-row span {
  font-weight: 600;
  color: var(--color-text-primary);
}

.biography-section {
  margin-top: var(--spacing-xl);
}

.biography-section strong {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-lg);
  color: var(--color-text-primary);
}

.biography-section p {
  background: var(--color-bg);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  line-height: 1.6;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

.no-selection {
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--color-text-secondary);
  margin-top: 100px;
  font-size: var(--font-size-lg);
}
</style>
