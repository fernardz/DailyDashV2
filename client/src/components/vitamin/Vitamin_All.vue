<template>
<div>
  <div class="d-flex flex-wrap">
    <div v-for="vit in vitAll" style='padding: 1px' :key="vit.id">
      <b-button-group>
        <b-button size='s'
        variant="outline-primary">{{vit.name}}</b-button>
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
</div>
</template>
<script>
export default {
  name: 'VitAll',
  computed: {
    vitAll() {
      return this.$store.state.vitamins;
    },
  },
  mounted() {
    this.$store.dispatch('getVitamins');
  },
};
</script>
