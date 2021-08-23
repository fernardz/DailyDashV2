<template>
  <div class="home">
    <Water/>
    <Vitamin/>
    <Strava/>
  </div>
</template>

<script>
// @ is an alias to /src
import Water from '@/components/Water.vue';
import Vitamin from '@/components/Vitamin.vue';
import Strava from '@/components/Strava.vue';
// eslint-disable-next-line

export default {
  name: 'DashBoard',
  components: {
    Water,
    Vitamin,
    Strava,
  },
};
</script>
