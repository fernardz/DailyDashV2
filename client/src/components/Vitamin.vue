<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-10">
              <h1> Vitamin Consumption </h1>
              <hr><br><br>
              <alert :message=message v-if="showMessage"></alert>
              <button type="button" class="btn btn-success btn-sm" v-b-modal.vitamin-modal>
                Create Vitamin
              </button>
              <button type="button" class="btn btn-success btn-sm" v-b-modal.vitamin-modal>
                Add Record
              </button>
              <br><br>
              <br><br>
              <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Vitamin</th>
                        <th scope="col">Date</th>
                        <th scope="col">Amount</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(vitamin, index) in vitamins" :key="index">
                        <td>{{vitamin.name}}</td>
                        <template v-if="vitamin.goals.length>0">
                          <td>{{vitamin.goals[0].qty}}</td>
                        </template>
                        <template v-else>
                          <td>No Goal Set</td>
                        </template>
                        <td><button type="button" class="btn btn-danger btn-sm"
                        @click="onDeleteVitamin(vitamin)">Delete</button></td>
                    </tr>

                </tbody>
              </table>
            </div>
      </div>

    <b-modal ref="addVitaminModal"
          id="vitamin-modal"
          title="Add a new water record"
          hide-footer>
    <b-form @submit="onSubmitVitamin" @reset="onResetVitamin" class="w-100">
    <b-form-group id="form-v-group"
                  label="Name:"
                  label-for="form-v-input">
        <b-form-input id="form-v-input"
                      type="string"
                      v-model="addVitaminForm.name"
                      required
                      placeholder="Enter name">
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    </b-modal>

  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
// eslint-disable-next-line
import Tools from './mixins/Tools';

export default {
  name: 'Vitamin',
  mixins: ['Tools'],
  data() {
    return {
      addVitaminForm: {
        name: '',
      },
      vitamins: [],
      current: 0,
      current_goal: 0,
      message: '',
      showMessage: false,
    };
  },

  components: {
    alert: Alert,
  },

  methods: {
    getVitamins() {
      const path = 'http://localhost:8000/vitamins/';
      axios.get(path)
        .then((res) => {
          this.vitamins = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    removeVitamin(vitID) {
      const path = `http://localhost:8000/vitamins/${vitID}`;
      axios.delete(path)
        .then(() => {
          this.getVitamins();
          this.message = 'Vitamin Deleted!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getVitamins();
        });
    },
    addVitamins(payload) {
      const path = 'http://localhost:8000/vitamins/';
      axios.post(path, payload)
        .then(() => {
          this.getVitamins();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onDeleteVitamin(vitamin) {
      this.removeVitamin(vitamin.id);
    },
    initVForm() {
      this.addVitamins.name = '';
    },
    onSubmitVitamin(evt) {
      evt.preventDefault();
      this.$refs.addVitaminModal.hide();
      const payload = {
        name: this.addVitaminForm.name,
      };
      this.addVitamins(payload);
      this.initVitForm();
    },
    onResetVitamin(evt) {
      evt.preventDefault();
      this.$refs.addVitaminModal.hide();
      this.initVForm();
    },
  },
  created() {
    this.getVitamins();
  },
};
</script>
