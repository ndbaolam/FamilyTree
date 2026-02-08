<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useFamilyStore } from '@/stores/familyStore';
import EditPersonModal from '@/components/EditPersonModal.vue';

const store = useFamilyStore();
const activeTab = ref('people');
const showEditModal = ref(false);
const selectedPerson = ref<any>(null);

onMounted(() => {
  store.fetchTree();
});

const sortedPeople = computed(() => {
    return [...store.people].sort((a, b) => a.name.localeCompare(b.name));
});

function openAddPerson() {
    selectedPerson.value = null;
    showEditModal.value = true;
}

function editPerson(person: any) {
    selectedPerson.value = person;
    showEditModal.value = true;
}

function deletePerson(id: string) {
    if (confirm('Are you sure you want to delete this person? This will also remove all their relationships.')) {
        store.deletePerson(id);
    }
}

function deleteRelationship(id: string) {
    if (confirm('Are you sure you want to delete this relationship?')) {
        store.deleteRelationship(id);
    }
}
</script>

<template>
  <div class="admin-dashboard">
    <div class="admin-header">
      <h1>Admin Dashboard</h1>
       <div class="nav-tabs">
        <button class="tab-btn" :class="{ active: activeTab === 'people' }" @click="activeTab = 'people'">People</button>
        <button class="tab-btn" :class="{ active: activeTab === 'relationships' }" @click="activeTab = 'relationships'">Relationships</button>
      </div>
       <button @click="store.logout(); $router.push('/')" class="btn">Logout</button>
    </div>

    <div class="dashboard-content">
        <!-- People Tab -->
        <div v-if="activeTab === 'people'">
             <div class="header-actions">
                <h2>People Management</h2>
                <button @click="openAddPerson" class="btn btn-primary">+ Add Person</button>
            </div>
            
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Avatar</th>
                            <th>Name</th>
                            <th>Gender</th>
                            <th>Birth Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="person in sortedPeople" :key="person.id">
                            <td>
                                <img :src="person.avatar_url || 'https://via.placeholder.com/40'" class="mini-avatar" />
                            </td>
                            <td>{{ person.name }}</td>
                            <td>{{ person.gender }}</td>
                            <td>{{ person.birth_date || '-' }}</td>
                            <td>
                                <button class="btn-sm" @click="editPerson(person)">Edit</button>
                                <button class="btn-sm btn-danger" @click="deletePerson(person.id)">Delete</button>
                            </td>
                        </tr>
                        <tr v-if="sortedPeople.length === 0">
                            <td colspan="5" class="text-center">No people found.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Relationships Tab -->
        <div v-if="activeTab === 'relationships'">
            <h2>Relationship Management</h2>
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Source ID</th>
                            <th>Type</th>
                            <th>Target ID</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="edge in store.edges" :key="edge.id">
                            <td>{{ edge.source }}</td>
                            <td><span class="badge">{{ edge.label }}</span></td>
                            <td>{{ edge.target }}</td>
                            <td>
                                <button @click="deleteRelationship(edge.id)" class="btn-sm btn-danger">Delete</button>
                            </td>
                        </tr>
                         <tr v-if="store.edges.length === 0">
                            <td colspan="4" class="text-center">No relationships found.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <EditPersonModal :show="showEditModal" :person="selectedPerson" @close="showEditModal = false" />
  </div>
</template>

<style scoped>
.admin-dashboard {
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: var(--color-bg);
}

.admin-header {
    background: var(--color-surface);
    border-bottom: 1px solid var(--color-border);
    padding: var(--spacing-md) var(--spacing-xl);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.admin-header h1 {
    margin: 0;
    font-size: var(--font-size-xl);
}

.nav-tabs {
    display: flex;
    gap: var(--spacing-md);
}

.tab-btn {
    background: none;
    border: none;
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-lg);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    color: var(--color-text-secondary);
}

.tab-btn.active {
    color: var(--color-primary);
    border-bottom-color: var(--color-primary);
    font-weight: 600;
}

.dashboard-content {
    flex: 1;
    padding: var(--spacing-xl);
    overflow-y: auto;
}

.header-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
}

.table-container {
    background: var(--color-surface);
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--color-border);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th, .data-table td {
    padding: var(--spacing-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

.data-table th {
    background: #f1f5f9;
    font-weight: 600;
    color: var(--color-text-secondary);
}

.mini-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.badge {
    background: #e0f2fe;
    color: #0369a1;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.85em;
    font-weight: 500;
}

.btn-sm {
    padding: 4px 8px;
    font-size: 0.9em;
    border: 1px solid var(--color-border);
    background: white;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 5px;
}

.btn-danger {
    color: var(--color-error);
    border-color: var(--color-error);
}

.btn-danger:hover {
    background: #fef2f2;
}

.text-center {
    text-align: center;
}
</style>
