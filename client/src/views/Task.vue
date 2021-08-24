<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <tdaily :daily_tasks=daily_tasks></tdaily>
      </div>
    </div>
  </div>
</template>
<script>
import TaskDaily from '@/components/tasks/Task_Day.vue';

export default {
  name: 'TaskDailyView',
  computed: {
    daily_tasks() {
      return this.$store.state.tasks_day;
    },
  },
  components: {
    tdaily: TaskDaily,
  },
  mounted() {
    this.$store.dispatch('getDailyTasks');
  },
};
</script>
