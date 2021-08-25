<template>
<div class=row>
  <div class=col-sm-2>
    <span><strong>Water</strong></span>
  </div>
  <div class=col-sm-10>
  <template v-if="current_water">
  <b-progress :max="current_water_goal.size" height="2rem">
    <b-progress-bar :value="current_water.sum">
        <span><strong>Water: {{ current_water.sum }} / {{ current_water_goal.size }}
          </strong></span>
    </b-progress-bar>
  </b-progress>
  </template>
  </div>
</div>
</template>

<script>
export default {
  name: 'WaterProgress',
  computed: {
    current_water() {
      return this.$store.state.current_water;
    },
    current_water_goal() {
      return this.$store.state.water_goal;
    },
  },
  mounted() {
    this.$store.dispatch('getCurrent');
    this.$store.dispatch('getCurrentGoal');
  },
};
</script>
