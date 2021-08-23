<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-10">
              <h1> Water Consumption </h1>
              <hr><br><br>
              <water></water>
              <hr>
              <alert :message=message v-if="showMessage"></alert>
              <button type="button" class="btn btn-success btn-sm" v-b-modal.water-modal>
                Add Record
              </button>
              <br><br>
              <div>{{ getCurrentDate() }}</div>
              <template v-if="current_water_goal">
                <h3>Current Water Consumption:
                   {{current_water.sum}} - {{current_water_goal.size}}</h3>
              </template>
              <template v-else>
                <h3>Current Water Consumption: {{current_water.sum}} / NO GOAL</h3>
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
import Water from '@/components/Water.vue';
import Alert from '@/components/Alert.vue';

export default {
  name: 'Water',
  mixins: [Water],
  components: {
    alert: Alert,
    water: Water,
  },
};
</script>
