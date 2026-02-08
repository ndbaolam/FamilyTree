<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { useFamilyStore } from '@/stores/familyStore';

const props = defineProps<{
  show: boolean;
  person?: any;
}>();

const emit = defineEmits(['close']);

const store = useFamilyStore();

const isEditing = computed(() => !!props.person);

const form = ref({
  name: '',
  gender: 'Male',
  birth_date: '',
  death_date: '',
  biography: '',
  avatar_url: ''
});

// Watch for changes in the person prop to populate the form
watch(() => props.person, (newPerson) => {
  if (newPerson) {
    form.value = {
      name: newPerson.name || '',
      gender: newPerson.gender || 'Male',
      birth_date: newPerson.birth_date || '',
      death_date: newPerson.death_date || '',
      biography: newPerson.biography || '',
      avatar_url: newPerson.avatar_url || ''
    };
  } else {
    resetForm();
  }
}, { immediate: true });

function resetForm() {
    form.value = {
    name: '',
    gender: 'Male',
    birth_date: '',
    death_date: '',
    biography: '',
    avatar_url: ''
  };
}

const selectedFile = ref<File | null>(null);

function handleFileUpload(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
        selectedFile.value = target.files[0] || null;
    }
}

async function save() {
  let personId = props.person?.id;

  if (isEditing.value && props.person) {
    await store.updatePerson(props.person.id, form.value);
  } else {
    const created = await store.createPerson(form.value);
    if (created) personId = created.id;
  }

  if (personId && selectedFile.value) {
      // Explicit check to satisfy TS
      await store.uploadAvatar(personId, selectedFile.value as File);
  }

  emit('close');
  resetForm();
  selectedFile.value = null;
}
</script>

<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal">
      <h2>{{ isEditing ? 'Edit Person' : 'Add Person' }}</h2>
      <form @submit.prevent="save">
        <div class="form-group">
          <label>Name:</label>
          <input v-model="form.name" required />
        </div>
        <div class="form-group">
          <label>Gender:</label>
          <select v-model="form.gender">
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>
        <div class="form-group">
          <label>Birth Date:</label>
          <input type="date" v-model="form.birth_date" />
        </div>
         <div class="form-group">
          <label>Death Date (Optional):</label>
          <input type="date" v-model="form.death_date" />
        </div>
        <div class="form-group">
          <label>Biography:</label>
          <textarea v-model="form.biography"></textarea>
        </div>
        <div class="form-group">
            <label>Avatar URL (or upload below):</label>
            <input v-model="form.avatar_url" placeholder="https://..." />
        </div>
         <div class="form-group">
            <label>Upload Avatar:</label>
            <input type="file" @change="handleFileUpload" accept="image/*" />
        </div>
        <div class="actions">
          <button type="button" @click="$emit('close')">Cancel</button>
          <button type="submit">Save</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal {
  background: var(--color-surface);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  width: 500px;
  max-width: 90%;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--color-border);
}

h2 {
  margin-top: 0;
  margin-bottom: var(--spacing-lg);
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
  text-align: center;
}

.form-group {
  margin-bottom: var(--spacing-md);
}

label {
  display: block;
  margin-bottom: var(--spacing-xs);
  font-weight: 600;
  color: var(--color-text-secondary);
  font-size: var(--font-size-lg);
}

input, select, textarea {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-lg); /* Larger text for inputs */
  background-color: var(--color-bg);
  color: var(--color-text-primary);
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

textarea {
  min-height: 120px;
  resize: vertical;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
}

button {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-lg);
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: background-color 0.2s;
}

button[type="button"] {
  background-color: transparent;
  color: var(--color-text-secondary);
  border: 2px solid var(--color-border);
}

button[type="button"]:hover {
  background-color: var(--color-bg);
  color: var(--color-text-primary);
}

button[type="submit"] {
  background-color: var(--color-primary);
  color: white;
}

button[type="submit"]:hover {
  background-color: var(--color-primary-hover);
}
</style>
