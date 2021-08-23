<template>
  <div class="hello">
    <waterprogress :water_goal=current_water_goal :current_water=current_water></waterprogress>
  </div>
</template>

<script>
import WaterProgress from '@/components/water/Water_Progress.vue';

export default {
  name: 'myStore',
  data() {
    return {
      msg: 'Welcome to my Vuex Store',
    };
  },
  computed: {
    waters() {
      return this.$store.state.waters;
    },
    current_water() {
      return this.$store.state.current_water;
    },
    current_water_goal() {
      return this.$store.state.water_goal;
    },
  },
  components: {
    waterprogress: WaterProgress,
  },
  mounted() {
    this.$store.dispatch('getWaters');
    this.$store.dispatch('getCurrent');
    this.$store.dispatch('getCurrentGoal');
  },
};
</script>
