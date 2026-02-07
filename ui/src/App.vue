<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
  overflow: hidden; /* Prevent scrolling on body, let vue flow handle it */
}
</style>
