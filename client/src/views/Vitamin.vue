<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-12">
            <vprogress></vprogress>
            <hr>
            <vall></vall>
          </div>
      </div>
  </div>
</template>

<script>
import VitaminProgress from '@/components/vitamin/Vitamin_Progress.vue';
import VitAll from '@/components/vitamin/Vitamin_All.vue';

export default {
  name: 'Vitamin',
  components: {
    vprogress: VitaminProgress,
    vall: VitAll,
  },
  mounted() {
    this.$store.dispatch('getCurrentVitamins');
  },
};
</script>
