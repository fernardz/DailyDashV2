<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-10">
              <h1> Water Consumption </h1>
              <hr><br><br>
              <button type="button" class="btn btn-success btn-sm">Add Record</button>
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
                        <td>NO</td>
                    </tr>

                </tbody>
              </table>
            </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Water',
  data() {
    return {
      waters: [],
      books: [],
    };
  },
  methods: {
    getWaters() {
      const path = 'http://localhost:8000/water/';
      axios.get(path)
        .then((res) => {
          console.log(res);
          this.waters = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getWaters();
  },
};
</script>
