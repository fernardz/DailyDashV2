<template>
<div>
  <div class="d-flex flex-wrap">
    <div v-for="vit in vitAll" style='padding: 1px' :key="vit.id">
      <b-button-group>
        <b-button size='s'
        variant="outline-primary">{{vit.name}}</b-button>
        <b-button size='s'
        variant="outline-info"><b-icon-pen></b-icon-pen></b-button>
        <b-button size='s' variant="outline-danger" @click="setSel(vit)" v-b-modal.del-conf>
          <b-icon-trash></b-icon-trash>
        </b-button>
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
  <b-modal ref="confirmDelete"
          id="del-conf"
          :title= "selVit.name"
          hide-footer>
    <b-button-group>
      <b-button type="submit" variant="primary" @click="onDel()">Delete</b-button>
      <b-button type="reset" variant="danger">Cancel</b-button>
    </b-button-group>
  </b-modal>
</div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'VitAll',
  data() {
    return {
      selVit: '',
    };
  },
  computed: {
    vitAll() {
      return this.$store.state.vitamins;
    },
  },
  methods: {
    setSel(vr) {
      this.selVit = vr;
    },
    onDel() {
      this.$refs.confirmDelete.hide();
      this.removeVit(this.selVit.id);
      this.selVit = '';
    },
    removeVit(vid) {
      const path = `http://192.168.1.181:8000/vitamins/${vid}`;
      axios.delete(path)
        .then(() => {
          this.$store.dispatch('getVitamins');
          this.$store.dispatch('getCurrentVitamins');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    this.$store.dispatch('getVitamins');
  },
};
</script>
