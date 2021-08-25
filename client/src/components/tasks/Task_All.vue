<template>
<div>
  <div class="d-flex flex-wrap">
    <div v-for="taska in tasksAll" style='padding: 1px' :key="taska.id">
      <b-button-group>
        <b-button size='s'
        variant="outline-primary" @click="onTaskSel(taska)">{{taska.desc}}</b-button>
        <b-button size='s'
        variant="outline-info"><b-icon-pen></b-icon-pen></b-button>
        <b-button size='s'
        variant="outline-danger"><b-icon-trash></b-icon-trash></b-button>
      </b-button-group>
    </div>
    <div>
    <b-button size='s' variant="outline-success">
      <b-icon-plus-circle>
      </b-icon-plus-circle>
    </b-button>
    </div>
  </div>
  <hr>
  <div>
    <div v-for="taskr in tasksSelRec" style='padding: 1px' :key="taskr.id">
      <b-button-group>
        <b-button size='s'
        variant="outline-primary" >{{taskr.date}}</b-button>
        <b-button size='s'
        variant="outline-danger"><b-icon-trash></b-icon-trash></b-button>
      </b-button-group>
    </div>
    <b-button size='s' variant="outline-success">
      <b-icon-plus-circle>
      </b-icon-plus-circle>
    </b-button>
  </div>
  <hr>
</div>
</template>
<script>
export default {
  name: 'TaskAll',
  data() {
    return {
      task_to_pull: 1,
    };
  },
  computed: {
    tasksAll() {
      return this.$store.state.tasks;
    },
    tasksSelRec() {
      return this.$store.getters.getTaskRecordsById(this.task_to_pull);
    },
  },
  methods: {
    onTaskSel(task) {
      this.task_to_pull = task.id;
    },
  },
  mounted() {
    this.$store.dispatch('getTasks');
    this.$store.dispatch('getTaskRecords');
  },
};
</script>
