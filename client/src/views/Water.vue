<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-8">
            <waterprogress></waterprogress>
          </div>
          <div class="col-sm-4">
            <watercontrol></watercontrol>
          </div>
      </div>
      <hr>
      <div class="row">
        <div class="col-sm-12">
          <waterrecords></waterrecords>
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
  components: {
    waterprogress: WaterProgress,
    watercontrol: WaterControl,
    waterrecords: WaterRecords,
  },
  mounted() {
    this.$store.dispatch('getWaters');
    this.$store.dispatch('getCurrent');
    this.$store.dispatch('getCurrentGoal');
  },
};
</script>
