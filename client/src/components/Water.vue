<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-10">
              <h1> Water Consumption </h1>
              <hr><br><br>
              <alert :message=message v-if="showMessage"></alert>
              <button type="button" class="btn btn-success btn-sm" v-b-modal.water-modal>
                Add Record
              </button>
              <br><br>
              <div>{{ getCurrentDate() }}</div>
              <template v-if="current_goal">
                <h3>Current Water Consumption: {{current.sum}} - {{current_goal.size}}</h3>
              </template>
              <template v-else>
                <h3>Current Water Consumption: {{current.sum}} / NO GOAL</h3>
              </template>
              <br><br>
              <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Date</th>
                        <th scope="col">Amount</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(water, index) in waters" :key="index">
                        <td>{{water.date}}</td>
                        <td>{{water.size}}</td>
                        <td><button type="button" class="btn btn-danger btn-sm"
                        @click="onDeleteWater(water)">Delete</button></td>
                    </tr>

                </tbody>
              </table>
            </div>
      </div>

    <b-modal ref="addWaterModal"
          id="water-modal"
          title="Add a new water record"
          hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-date-group"
                  label="Date:"
                  label-for="form-date-input">
        <b-form-input id="form-date-input"
                      type="date"
                      v-model="addWaterForm.date"
                      required
                      placeholder="Enter date">
        </b-form-input>
      </b-form-group>
      <b-form-group id="form-size-group"
                    label="Size:"
                    label-for="form-size-input">
          <b-form-input id="form-size-input"
                        type="number"
                        v-model="addWaterForm.size"
                        required
                        placeholder="Enter amount drank">
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
import Tools from './mixins/Tools';

export default {
  name: 'Water',
  mixins: [Tools],
  data() {
    return {
      addWaterForm: {
        date: '',
        size: '',
      },
      waters: [],
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
    getWaters() {
      const path = 'http://localhost:8000/water';
      axios.get(path)
        .then((res) => {
          this.waters = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getCurrent() {
      const path = `http://localhost:8000/water/get_day_results/${this.getCurrentDate()}`;
      axios.get(path)
        .then((res) => {
          this.current = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getCurrentGoal() {
      const path = 'http://localhost:8000/water_goal/current/';
      axios.get(path)
        .then((res) => {
          // eslint-disable-next-line
          console.log(res.data);
          this.current_goal = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    removeWater(waterID) {
      const path = `http://localhost:8000/water/${waterID}`;
      axios.delete(path)
        .then(() => {
          this.getWaters();
          this.message = 'Water Record Deleted!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getWaters();
          this.getCurrent();
        });
    },
    addWater(payload) {
      const path = 'http://localhost:8000/water';
      axios.post(path, payload)
        .then(() => {
          this.getWaters();
          this.getCurrent();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onDeleteWater(water) {
      this.removeWater(water.id);
    },
    initForm() {
      this.addWaterForm.date = '';
      this.addWaterForm.size = 0;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addWaterModal.hide();
      const payload = {
        date: this.addWaterForm.date,
        size: this.addWaterForm.size,
      };
      this.addWater(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addWaterModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getWaters();
    this.getCurrent();
    this.getCurrentGoal();
  },
};
</script>
