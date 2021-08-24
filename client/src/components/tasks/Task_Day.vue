<template>
  <div>
      <div class="row" v-for="daily_task in daily_tasks" :key="daily_task.id">
        <div class="col-sm-12">
          <template v-if="daily_task.status">
            <b-button pill size='s' class="w-100" variant="outline-success">
              {{daily_task.desc}}
            </b-button>
          </template>
          <template v-else>
            <b-button pill size='s' class="w-100" variant="outline-danger">
              {{daily_task.desc}}
            </b-button>
          </template>
        </div>
      </div>
  </div>
</template>
<script>
export default {
  name: 'TasksDaily',
  props: ['daily_tasks'],
};
</script>
