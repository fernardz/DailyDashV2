<template>
  <div class="container">
    <actdaily></actdaily>
  </div>
</template>
<script>
import ActDaily from '@/components/activity/Activity_Day.vue';

export default {
  name: 'ActView',
  components: {
    actdaily: ActDaily,
  },
};
</script>
