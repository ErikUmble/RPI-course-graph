<script setup lang="ts">
import { onMounted, ref } from "vue";
import cytoscape from "cytoscape";

const cyContainer = ref(null);

onMounted(() => {
  const cy = cytoscape({
    container: cyContainer.value, // the DOM element

    elements: [
      { data: { id: "a" } },
      { data: { id: "b" } },
      { data: { id: "ab", source: "a", target: "b" } },
    ],

    style: [
      {
        selector: "node",
        style: {
          "background-color": "#0074D9",
          label: "data(id)",
          color: "white",
          "text-valign": "center",
          "text-halign": "center",
        },
      },
      {
        selector: "edge",
        style: {
          width: 3,
          "line-color": "#aaa",
          "target-arrow-color": "#aaa",
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
        },
      },
    ],

    layout: {
      name: "grid",
      rows: 1,
    },
  });
});
</script>

<template>
  <div ref="cyContainer" style="width: 600px; height: 400px; border: 1px solid #ddd;" />
</template>

<style scoped></style>
