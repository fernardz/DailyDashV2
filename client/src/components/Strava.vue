<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-10">
              <h1> Activities </h1>
              <hr><br><br>
              <alert :message=message v-if="showMessage"></alert>
              <div>{{ getCurrentDate() }}</div>
                <h3>Activity Count:</h3>
              <br><br>
              <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Date</th>
                        <th scope="col">Minutes</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(act, index) in acts" :key="index">
                        <td>{{act.start_date | formatDate}}</td>
                        <td>{{act.id}}</td>
                    </tr>

                </tbody>
              </table>
            </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Tools from './mixins/Tools';

export default {
  name: 'Strava',
  mixins: [Tools],
  data() {
    return {
      acts: [],
      message: '',
      showMessage: false,
    };
  },

  components: {
    alert: Alert,
  },

  methods: {
    getActs() {
      const path = 'http://localhost:8000/strava';
      axios.get(path)
        .then((res) => {
          this.acts = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getActs();
  },
};
</script>
