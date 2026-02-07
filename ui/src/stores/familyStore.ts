import { defineStore } from 'pinia';
import api from '../api';
import type { Node, Edge } from '@vue-flow/core';

interface Person {
    id: string;
    name: string;
    gender: string;
    birth_date?: string;
    death_date?: string;
    biography?: string;
    avatar_url?: string;
}

interface GraphData {
    nodes: any[];
    edges: any[];
}

export const useFamilyStore = defineStore('family', {
    state: () => ({
        people: [] as Person[],
        nodes: [] as Node[],
        edges: [] as Edge[],
        loading: false,
        error: null as string | null,
        isAdmin: false,
    }),
    actions: {
        async fetchTree() {
            this.loading = true;
            try {
                const response = await api.get<GraphData>('/tree');

                // Parse edges first to build the graph structure
                const rawEdges = response.data.edges.map(e => ({
                    id: e.id || `${e.source}-${e.target}`,
                    source: e.source,
                    target: e.target,
                    label: e.label,
                    type: 'smoothstep',
                    animated: true,
                    data: e.data || {} // Includes 'order'
                }));

                // Build Layout
                const layoutNodes = this.calculateLayout(response.data.nodes, rawEdges);

                this.nodes = layoutNodes;
                this.edges = rawEdges;
            } catch (err: any) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },
        calculateLayout(nodes: any[], edges: any[]) {
            const NODE_WIDTH = 200;
            const NODE_HEIGHT = 100;
            const LEVEL_HEIGHT = 150;

            // Build adjacency list
            const childrenMap: Record<string, any[]> = {};
            const takenTargets = new Set<string>();

            edges.forEach(edge => {
                if (!childrenMap[edge.source]) {
                    childrenMap[edge.source] = [];
                }
                // Store edge data with the child ID so we can sort by it
                const order = (edge.data && typeof edge.data.order === 'number') ? edge.data.order : 999;
                childrenMap[edge.source]?.push({
                    id: edge.target,
                    order: order
                });
                takenTargets.add(edge.target);
            });

            // Identify roots (nodes not in target list)
            const roots = nodes.filter(n => !takenTargets.has(n.id));

            // Helper to sort children
            const getSortedChildren = (nodeId: string) => {
                const children = childrenMap[nodeId] || [];
                return children.sort((a, b) => a.order - b.order).map(c => c.id);
            };

            const nodePositions: Record<string, { x: number, y: number }> = {};
            let leafCounter = 0;

            // Recursive function to assign positions
            // Returns the 'x' center of the subtree rooted at nodeId
            const layoutNode = (nodeId: string, level: number): number => {
                const childrenIds = getSortedChildren(nodeId);

                let xPos = 0;
                if (childrenIds.length === 0) {
                    // Leaf node
                    xPos = leafCounter * NODE_WIDTH;
                    leafCounter++;
                } else {
                    // Parent node: position is average of children
                    const childXVals = childrenIds.map(childId => layoutNode(childId, level + 1));
                    const firstChildX = childXVals[0] ?? 0;
                    const lastChildX = childXVals[childXVals.length - 1] ?? 0;
                    xPos = (firstChildX + lastChildX) / 2;
                }

                nodePositions[nodeId] = { x: xPos, y: level * LEVEL_HEIGHT };
                return xPos;
            };

            // Run layout for each root (handling disconnected components by spacing them out)
            roots.forEach(root => {
                layoutNode(root.id, 0);
                // Add spacing between disconnected trees if needed (leafCounter handles it naturally)
                leafCounter++;
            });

            // Map back to Vue Flow nodes
            return nodes.map(n => {
                const pos = nodePositions[n.id] || { x: 0, y: 0 };
                return {
                    id: n.id,
                    position: pos,
                    data: n.data,
                    label: n.label
                };
            });
        },
        async createPerson(person: Omit<Person, 'id'>) {
            try {
                const response = await api.post<Person>('/people', person);
                this.people.push(response.data);
                await this.fetchTree();
            } catch (err: any) {
                this.error = err.message;
            }
        },
        async createRelationship(source: string, target: string, type: 'PARENT_OF' | 'MARRIED_TO') {
            try {
                await api.post('/relationships', {
                    from_person_id: source,
                    to_person_id: target,
                    relationship_type: type
                });
                await this.fetchTree();
            } catch (err: any) {
                this.error = err.message;
            }
        },
        async deleteRelationship(relationshipId: string) {
            try {
                await api.delete(`/relationships/${relationshipId}`);
                await this.fetchTree();
            } catch (err: any) {
                this.error = err.message;
            }
        },
        login(password: string) {
            if (password === 'admin123') {
                this.isAdmin = true;
                return true;
            }
            return false;
        },
        logout() {
            this.isAdmin = false;
        }
    },
});
