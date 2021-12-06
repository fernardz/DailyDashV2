<template>
  <div>
      <div class="row" v-for="daily_task in daily_tasks" :key="daily_task.id">
        <div class="col-sm-12" style="padding: 1px;">
          <template v-if="daily_task.status">
            <b-button pill size='s' class="w-100" variant="outline-success"
            style="font-size: 0.8em;"
            @click="onTaskToggle(daily_task)">
              {{daily_task.desc}}
            </b-button>
          </template>
          <template v-else>
            <b-button pill size='s' class="w-100" variant="outline-danger"
             style="font-size: 0.8em;"
            @click="onTaskToggle(daily_task)">
              {{daily_task.desc}}
            </b-button>
          </template>
        </div>
      </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'TasksDaily',
  computed: {
    daily_tasks() {
      const res = this.$store.state.tasks_day;
      // eslint-disable-next-line
      return res.sort((a, b) => ((a.status > b.status) ? -1 : 1));
    },
  },
  methods: {
    onTaskToggle(task) {
      let tstatus;
      if (task.status) {
        tstatus = false;
      } else {
        tstatus = true;
      }
      const payload = {
        date: task.date,
        status: tstatus,
        task_id: task.task_id,
      };
      this.updateTaskRecord(task.id, payload);
    },
    updateTaskRecord(tid, payload) {
      const path = `http://localhost:8000/task_record/${tid}`;
      axios.put(path, payload)
        .then(() => {
          this.$emit('clicked', true);
          this.$store.dispatch('getDailyTasks');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
  },
  mounted() {
    this.$store.dispatch('getDailyTasks');
  },
};
</script>
