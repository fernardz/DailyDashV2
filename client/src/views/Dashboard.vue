<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-8">
        <table class="table table-hover">
        <thead>
            <tr>
                <th scope="col">Vitamin</th>
                <th scope="col">Goal</th>
                <th scope="col">Amount</th>
            </tr>
        </thead>
        <tbody>
          <tr v-for="(s, index) in vsummary" :key="index">
          <td>{{s.name}}</td>
          <td>{{s.goal}}</td>
          <td>{{s.amount}}</td>
          </tr>
          </tbody>
        </table>
        <hr>
        <template v-if="current_goal">
          <h3>Current Water Consumption: {{current.sum}} - {{current_goal.size}}</h3>
        </template>
        <template v-else>
          <h3>Current Water Consumption: {{current.sum}} / NO GOAL</h3>
        </template>
      </div>
    </div>
    <div class="row">
      <Water/>
      <Strava/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Water from '@/components/Water.vue';
import Vitamin from '@/components/Vitamin.vue';
import Strava from '@/components/Strava.vue';
// eslint-disable-next-line

export default {
  name: 'DashBoard',
  mixins: [Vitamin, Water],
  components: {
    Strava,
  },
};
</script>
