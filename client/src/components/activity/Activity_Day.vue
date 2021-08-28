<template>
  <div class="row">
    <div class="col-sm-6">
    <b-icon-watch></b-icon-watch>{{ actSum.time}} min
    </div>
    <div class="col-sm-6">
    <b-icon-compass></b-icon-compass> {{ actSum.distance }} miles
    </div>
  </div>
</template>
<script>
export default {
  name: 'ActDaily',
  computed: {
    actSum() {
      return this.$store.state.act_sum;
    },
  },
  mounted() {
    this.$store.dispatch('getActSummary');
  },
};
</script>
