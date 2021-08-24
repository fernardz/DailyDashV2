<template>
<div>
  <template v-if="current_water">
  <b-progress :max="water_goal.size" height="2rem">
    <b-progress-bar :value="current_water.sum">
        <span><strong>Water: {{ current_water.sum.toFixed(2) }} / {{ water_goal.size }}
          </strong></span>
    </b-progress-bar>
  </b-progress>
  </template>
</div>
</template>

<script>
export default {
  name: 'WaterProgress',
  props: ['water_goal', 'current_water'],
};
</script>
