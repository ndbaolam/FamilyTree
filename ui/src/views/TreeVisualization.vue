<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { VueFlow, useVueFlow } from '@vue-flow/core';
import { Background } from '@vue-flow/background';
import { Controls } from '@vue-flow/controls';
import { useFamilyStore } from '@/stores/familyStore';
import PersonDetailsPanel from '@/components/PersonDetailsPanel.vue';

const store = useFamilyStore();
const { onConnect, addEdges, onNodeClick } = useVueFlow();
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
</style>

