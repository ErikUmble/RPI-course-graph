<script setup lang="ts">
import { onMounted, ref } from "vue";
import cytoscape from "cytoscape";
import fcose from "cytoscape-fcose";
import courseData from "../data/aggregated.json";

cytoscape.use(fcose);

const cyContainer = ref(null);

onMounted(() => {

  const courses = Object.keys(courseData).map((courseId) => ({
    data: { id: courseId, label: courseId },
  }));

  const prereqs = Object.entries(courseData).map(([course, info]) =>
    info.prereqs.filter(
      (prereq) => Object.keys(courseData).includes(prereq)
    ).map(prereq => ({
      data: {
        id: `${prereq}->${course}`,
        source: prereq,
        target: course
      }
    }))
  ).flat();

  console.log(courses);
  console.log(prereqs);

  const cy = cytoscape({
    container: cyContainer.value, // the DOM element

    elements: [...courses, ...prereqs],

    style: [
      {
        selector: "node",
        style: {
          "background-color": "#0074D9",
          label: "data(id)",
          color: "white",
          "text-valign": "center",
          "text-halign": "center",
          width: 80,
          height: 80,
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
  });
  const layoutOptions = {
    name: "fcose",
    nodeRepulsion: 10000,
    idealEdgeLength: 100,
  };
  cy.layout(layoutOptions).run();
});
</script>

<template>
  <div ref="cyContainer" style="width: 600px; height: 400px; border: 1px solid #ddd;" />
</template>

<style scoped></style>
