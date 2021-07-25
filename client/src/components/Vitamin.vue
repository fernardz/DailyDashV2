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
                        <td>{{vitamin.name}}</td>
                        <td><button type="button" class="btn btn-danger btn-sm"
                        >Delete</button></td>
                    </tr>

                </tbody>
              </table>
            </div>
      </div>

    <b-modal ref="addVitaminModal"
          id="vitamin-modal"
          title="Add a new water record"
          hide-footer>
    <b-form class="w-100">
    <b-form-group id="form-date-group"
                  label="Name:"
                  label-for="form-date-input">
        <b-form-input id="form-date-input"
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
  },
  created() {
    this.getVitamins();
  },
};
</script>
