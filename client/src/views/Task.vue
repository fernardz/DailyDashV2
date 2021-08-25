<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <tdaily></tdaily>
        <hr>
        <tall></tall>
      </div>
    </div>
  </div>
</template>
<script>
import TaskDaily from '@/components/tasks/Task_Day.vue';
import TaskAll from '@/components/tasks/Task_All.vue';

export default {
  name: 'TaskDailyView',
  components: {
    tdaily: TaskDaily,
    tall: TaskAll,
  },
};
</script>
