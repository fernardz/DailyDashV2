<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-8">
            <waterprogress :water_goal=current_water_goal
            :current_water=current_water></waterprogress>
          </div>
          <div class="col-sm-4">
            <watercontrol @clicked="watercontrolClicked()"></watercontrol>
          </div>
      </div>
      <hr>
      <div class="row">
        <div class="col-sm-12">
          <waterrecords :waters=waters></waterrecords>
        </div>
      </div>
  </div>
</template>

<script>
import WaterProgress from '@/components/water/Water_Progress.vue';
import WaterControl from '@/components/water/Water_Control.vue';
import WaterRecords from '@/components/water/Water_Records.vue';

export default {
  name: 'Water',
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
    watercontrol: WaterControl,
    waterrecords: WaterRecords,
  },
  methods: {
    watercontrolClicked() {
      this.$store.dispatch('getWaters');
      this.$store.dispatch('getCurrent');
      this.$store.dispatch('getCurrentGoal');
    },
  },
  mounted() {
    this.$store.dispatch('getWaters');
    this.$store.dispatch('getCurrent');
    this.$store.dispatch('getCurrentGoal');
  },
};
</script>
