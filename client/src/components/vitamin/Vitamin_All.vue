<template>
<div>
  <div class="d-flex flex-wrap">
    <div v-for="vit in vitAll" style='padding: 1px' :key="vit.id">
      <b-button-group>
        <b-button size='s'
        variant="outline-primary">{{vit.name}}</b-button>
        <b-button size='s'
        variant="outline-info" @click="setSel(vit)" v-b-modal.create-goal>
        <b-icon-trophy>
        </b-icon-trophy></b-button>
        <b-button size='s' variant="outline-danger" @click="setSel(vit)" v-b-modal.del-conf>
          <b-icon-trash></b-icon-trash>
        </b-button>
      </b-button-group>
    </div>
    <div style='padding: 1px'>
      <b-button size='s' variant="outline-success" v-b-modal.create-vit>
        <b-icon-plus-circle>
        </b-icon-plus-circle>
      </b-button>
    </div>
  </div>
  <hr>
<!-- delete modal -->
  <b-modal ref="confirmDelete"
          id="del-conf"
          :title= "selVit.name"
          hide-footer>
    <b-button-group>
      <b-button type="submit" variant="primary" @click="onDel()">Delete</b-button>
      <b-button type="reset" variant="danger">Cancel</b-button>
    </b-button-group>
  </b-modal>
<!-- create vitamin modal -->
  <b-modal ref="createVitamin"
          id="create-vit"
          title= "Create New Vitamin"
          hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-size-group"
                      label="Vitamin Name:"
                      label-for="form-name-input">
            <b-form-input id="form-size-input"
                          type="text"
                          v-model="addVitForm.name"
                          required
                          placeholder="Enter Vitamin Name">
            </b-form-input>
      </b-form-group>
      <b-button-group>
        <b-button type="submit" variant="primary">Create</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-button-group>
    </b-form>
  </b-modal>
<!-- create vitamin goal modal -->
  <b-modal ref="createVitaminGoal"
          id="create-goal"
          title= "Create New Vitamin"
          hide-footer>
    <b-form @submit="onSubmitGoal" @reset="onReset" class="w-100">
      <b-form-group id="form-size-group"
                      label="Goal:"
                      label-for="form-name-input">
            <b-form-input id="form-size-input"
                          type="number"
                          v-model="addVitGoalForm.qty"
                          required
                          placeholder="Enter Amount">
            </b-form-input>
      </b-form-group>
      <b-button-group>
        <b-button type="submit" variant="primary">Create</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-button-group>
    </b-form>
  </b-modal>

</div>
</template>
<script>
import axios from 'axios';
import Tools from '@/components/mixins/Tools';

export default {
  name: 'VitAll',
  mixins: [Tools],
  data() {
    return {
      selVit: '',
      addVitGoalForm: {
        date: this.getCurrentDate(),
        qty: 0,
      },
      addVitForm: {
        name: '',
      },
    };
  },
  computed: {
    vitAll() {
      return this.$store.state.vitamins;
    },
  },
  methods: {
    initVitForm() {
      this.addVitForm.name = '';
    },
    initVitGoalForm() {
      this.addVitGoalForm.date = this.getCurrentDate();
      this.addVitGoalForm.qty = 0;
    },
    setSel(vr) {
      this.selVit = vr;
    },
    onDel() {
      this.$refs.confirmDelete.hide();
      this.removeVit(this.selVit.id);
      this.selVit = '';
    },
    removeVit(vid) {
      const path = `http://rasp-srv:8000/vitamins/${vid}`;
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
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.createVitamin.hide();
      const payload = {
        name: this.addVitForm.name,
      };
      this.addVit(payload);
      this.initVitForm();
    },
    onSubmitGoal(evt) {
      evt.preventDefault();
      this.$refs.createVitaminGoal.hide();
      const payload = {
        qty: this.addVitGoalForm.qty,
        date: this.addVitGoalForm.date,
      };
      this.addVitGoal(this.selVit.id, payload);
      this.initVitGoalForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.createVitamin.hide();
      this.$refs.createVitaminGoal.hide();
      this.initVitForm();
    },
    addVit(payload) {
      const path = 'http://rasp-srv:8000/vitamins/';
      axios.post(path, payload)
        .then(() => {
          this.$emit('clicked', true);
          this.$store.dispatch('getVitamins');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    addVitGoal(vid, payload) {
      const path = `http://rasp-srv:8000/vitamins/goal/?vit_id=${vid}`;
      axios.post(path, payload)
        .then(() => {
          this.$emit('clicked', true);
          this.$store.dispatch('getVitamins');
          this.$store.dispatch('getCurrentVitamins');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
  },
  mounted() {
    this.initVitForm();
    this.initVitGoalForm();
    this.$store.dispatch('getVitamins');
  },
};
</script>
