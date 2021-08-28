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
        <div class="col-sm-8" style="overflow-y: scroll; height: 180px">
            <vprogress >
            </vprogress>
        </div>
        <div class="col-sm-4" style="overflow-y: scroll; height: 180px">
            <tdaily></tdaily>
        </div>
      </div>
      <hr>
      <div class="row">
        <div class="col-sm-12">
          <actdaily></actdaily>
        </div>
      </div>
  </div>
</template>

<script>
// Water Module
import WaterProgress from '@/components/water/Water_Progress.vue';
import WaterControl from '@/components/water/Water_Control.vue';

// Vitamin Module
import VitaminProgress from '@/components/vitamin/Vitamin_Progress.vue';

// Task Module
import TaskDaily from '@/components/tasks/Task_Day.vue';

// Activity Module
import ActDaily from '@/components/activity/Activity_Day.vue';

export default {
  name: 'Dashboard',
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
    // water setion
    vitamin_summary() {
      return this.$store.state.vitamin_summary;
    },
  },
  components: {
    waterprogress: WaterProgress,
    watercontrol: WaterControl,
    // vitamin section
    vprogress: VitaminProgress,
    // task section
    tdaily: TaskDaily,
    // activity section
    actdaily: ActDaily,
  },
  methods: {
    watercontrolClicked() {
      this.$store.dispatch('getCurrent');
      this.$store.dispatch('getCurrentGoal');
    },
    vcontrolClicked() {
      this.$store.dispatch('getCurrentVitamins');
    },
  },
  mounted() {
    this.$store.dispatch('getCurrent');
    this.$store.dispatch('getCurrentGoal');
    // vitamin section
    this.$store.dispatch('getCurrentVitamins');
  },
};
</script>
