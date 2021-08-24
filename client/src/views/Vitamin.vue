<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-12">
            <vprogress :vitamin_summary=vitamin_summary @clicked="vcontrolClicked()">
            </vprogress>
          </div>
      </div>
      <hr>
  </div>
</template>

<script>
import VitaminProgress from '@/components/vitamin/Vitamin_Progress.vue';

export default {
  name: 'Vitamin',
  data() {
    return {
      msg: 'Welcome to my Vuex Store',
    };
  },
  computed: {
    vitamin_summary() {
      return this.$store.state.vitamin_summary;
    },
  },
  components: {
    vprogress: VitaminProgress,
  },
  methods: {
    vcontrolClicked() {
      this.$store.dispatch('getCurrentVitamins');
    },
  },
  mounted() {
    this.$store.dispatch('getCurrentVitamins');
  },
};
</script>
