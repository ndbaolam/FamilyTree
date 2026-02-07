<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { VueFlow, useVueFlow } from '@vue-flow/core';
import { Background } from '@vue-flow/background';
import { Controls } from '@vue-flow/controls';
import { useFamilyStore } from '@/stores/familyStore';
import EditPersonModal from '@/components/EditPersonModal.vue';
import PersonDetailsPanel from '@/components/PersonDetailsPanel.vue';

const store = useFamilyStore();
const { onConnect, addEdges, onNodeClick } = useVueFlow();
const showAddPersonModal = ref(false);
const selectedPerson = ref(null);
const isPanelOpen = ref(false);

onMounted(() => {
  store.fetchTree();
});

onConnect(async (params) => {
    if (store.isAdmin && params.source && params.target) {
        await store.createRelationship(params.source, params.target, 'PARENT_OF');
    }
});

onNodeClick((event) => {
  const node = event.node;
  selectedPerson.value = node.data;
  isPanelOpen.value = true;
});

</script>

<template>
  <div style="height: 100vh; width: 100%; position: relative; overflow: hidden;">
    <div v-if="store.isAdmin" class="controls-overlay">
      <button @click="showAddPersonModal = true">Add Person</button>
    </div>
    
    <VueFlow
      v-model:nodes="store.nodes"
      v-model:edges="store.edges"
      fit-view-on-init
      class="basicflow"
      :default-edge-options="{ type: 'smoothstep', animated: true }"
      :nodes-connectable="store.isAdmin"
    >
      <Background />
      <Controls />
    </VueFlow>

    <EditPersonModal :show="showAddPersonModal" @close="showAddPersonModal = false" />
    <PersonDetailsPanel 
      :person="selectedPerson" 
      :is-open="isPanelOpen" 
      @close="isPanelOpen = false" 
    />
  </div>
</template>

<style>
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/controls/dist/style.css';

/* Override Vue Flow defaults for better contrast */
.vue-flow__node {
  font-size: var(--font-size-lg); /* Larger text in nodes */
}

/* Custom styles for this view */
.controls-overlay {
  position: absolute;
  top: var(--spacing-lg);
  left: var(--spacing-lg);
  z-index: 10;
}

.controls-overlay button {
  background-color: var(--color-primary);
  color: white;
  padding: var(--spacing-md) var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  font-size: var(--font-size-xl);
  font-weight: 600;
  border: none;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  transition: transform 0.2s, background-color 0.2s;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.controls-overlay button:hover {
  background-color: var(--color-primary-hover);
  transform: translateY(-2px);
}

.controls-overlay button::before {
  content: "+";
  font-size: 1.5em;
  line-height: 1;
}
</style>

