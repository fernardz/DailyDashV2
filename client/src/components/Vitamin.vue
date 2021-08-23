<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-10">
              <h1> Vitamin Consumption </h1>
              <hr><br>
              <alert :message=message v-if="showMessage"></alert>
              <hr>
              <button type="button" class="btn btn-success btn-sm" v-b-modal.vitamin-modal>
                Create Vitamin
              </button>
              <br><br>
              <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Vitamin</th>
                        <th scope="col">Goal</th>
                        <th></th>
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
                          <td><button type="button" class="btn btn-danger btn-sm"
                          @click="onEditGoal(vitamin)"
                        v-b-modal.vitamin-goal>Set Goal</button></td>
                        </template>
                        <td><button type="button" class="btn btn-danger btn-sm"
                          @click="onAddRecord(vitamin)"
                        v-b-modal.vitamin-record>Add Record</button></td>
                        <td><button type="button" class="btn btn-danger btn-sm"
                        @click="onDeleteVitamin(vitamin)">Delete</button></td>
                    </tr>
                </tbody>
              </table>
              <hr>
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
                  <template v-for="vitamin in vitamins">
                    <tr v-for="(record, index) in vitamin.records" :key="index">
                        <td>{{vitamin.name}}</td>
                        <td>{{record.date}}</td>
                        <td>{{record.qty}}</td>
                        <td><button type="button" class="btn btn-danger btn-sm"
                        @click="onDeleteRecord(record)">Delete</button></td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
      </div>

    <b-modal ref="addVitaminModal"
          id="vitamin-modal"
          title="Create New Vitamin"
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

    <b-modal ref="addVitaminGoalModal"
          id="vitamin-goal"
          :title="'Add Goal for ' + addVitaminGoalForm.vitamin.name"
          hide-footer>
    <b-form @submit="onSubmitVitaminGoal" @reset="onResetVitaminGoal" class="w-100">
    <b-form-group id="form-v-group"
                  label="Amount:"
                  label-for="form-v-input">
        <b-form-input id="form-v-input"
                      type="number"
                      v-model="addVitaminGoalForm.qty"
                      required
                      placeholder="Enter amount">
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    </b-modal>

    <b-modal ref="addVitaminRecordModal"
          id="vitamin-record"
          :title="'Add Record for ' + addVitaminRecordForm.vitamin.name"
          hide-footer>
    <b-form @submit="onSubmitVitaminRecord" @reset="onResetVitaminRecord" class="w-100">
    <b-form-group id="form-v-group"
                  label="Date:"
                  label-for="form-v-input">
        <b-form-input id="form-v-input"
                      type="date"
                      v-model="addVitaminRecordForm.date"
                      required
                      placeholder="Enter date">
        </b-form-input>
      </b-form-group>

      <b-form-group id="form-v-group"
                  label="Amount:"
                  label-for="form-v-input">
        <b-form-input id="form-v-input"
                      type="number"
                      v-model="addVitaminRecordForm.qty"
                      required
                      placeholder="Enter amount">
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
  name: 'Vitamin',
  mixins: [Tools],
  data() {
    return {
      addVitaminForm: {
        name: '',
      },
      addVitaminGoalForm: {
        vitamin: '',
        qty: '',
      },
      addVitaminRecordForm: {
        vitamin: '',
        date: this.getCurrentDate(),
        qty: '',
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
      const path = 'http://192.168.1.181:8000/vitamins/';
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
      const path = `http://192.168.1.181:8000/vitamins/${vitID}`;
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
    removeRecord(vitID) {
      const path = `http://192.168.1.181:8000/vitamins/record/${vitID}`;
      axios.delete(path)
        .then(() => {
          this.getVitamins();
          this.message = 'Vitamin Record Deleted!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getVitamins();
        });
    },
    addVitamins(payload) {
      const path = 'http://192.168.1.181:8000/vitamins/';
      axios.post(path, payload)
        .then(() => {
          this.getVitamins();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    addVitaminGoal(vid, payload) {
      const path = `http://192.168.1.181:8000/vitamins/goal/?vit_id=${vid}`;
      axios.post(path, payload)
        .then(() => {
          this.getVitamins();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    addVitaminRecord(vid, payload) {
      const path = `http://192.168.1.181:8000/vitamins/record/?vit_id=${vid}`;
      axios.post(path, payload)
        .then(() => {
          this.getVitamins();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onEditGoal(vitamin) {
      this.addVitaminGoalForm.vitamin = vitamin;
    },
    onAddRecord(vitamin) {
      this.addVitaminRecordForm.vitamin = vitamin;
    },
    onDeleteVitamin(vitamin) {
      this.removeVitamin(vitamin.id);
    },
    onDeleteRecord(record) {
      this.removeRecord(record.id);
    },
    initVForm() {
      this.addVitamins.name = '';
    },
    initVGForm() {
      this.addVitaminGoalForm.vid = '';
      this.addVitaminGoalForm.qty = '';
    },
    initVRForm() {
      this.addVitaminRecordForm.vid = '';
      this.addVitaminRecordForm.qty = '';
      this.addVitaminRecordForm.date = this.getCurrentDate();
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
    onSubmitVitaminGoal(evt) {
      evt.preventDefault();
      this.$refs.addVitaminGoalModal.hide();
      const payload = {
        date: this.getCurrentDate(),
        qty: this.addVitaminGoalForm.qty,
      };
      this.addVitaminGoal(this.addVitaminGoalForm.vitamin.id, payload);
      this.initVGForm();
    },
    onSubmitVitaminRecord(evt) {
      evt.preventDefault();
      this.$refs.addVitaminRecordModal.hide();
      const payload = {
        date: this.addVitaminRecordForm.date,
        qty: this.addVitaminRecordForm.qty,
      };
      this.addVitaminRecord(this.addVitaminRecordForm.vitamin.id, payload);
      this.initVRForm();
    },
    onResetVitamin(evt) {
      evt.preventDefault();
      this.$refs.addVitaminModal.hide();
      this.initVForm();
    },
    onResetVitaminGoal(evt) {
      evt.preventDefault();
      this.$refs.addVitaminGoalModal.hide();
      this.initVGForm();
    },
    onResetVitaminRecord(evt) {
      evt.preventDefault();
      this.$refs.addVitaminRecordModal.hide();
      this.initVRForm();
    },
  },
  created() {
    this.getVitamins();
  },
};
</script>
