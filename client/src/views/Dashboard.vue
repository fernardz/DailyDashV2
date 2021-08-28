<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-8">
            <waterprogress></waterprogress>
          </div>
          <div class="col-sm-4">
            <watercontrol @clicked="watercontrolClicked()"></watercontrol>
          </div>
      </div>
      <hr>
      <div class="row">
        <div class="col-sm-8" style="overflow-y: scroll; height: 300px">
            <vprogress >
            </vprogress>
        </div>
        <div class="col-sm-4" style="overflow-y: scroll; height: 300px">
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
};
</script>
