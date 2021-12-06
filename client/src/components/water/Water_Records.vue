<template>
<div>
    <div>
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

</template>
<script>
import axios from 'axios';
import Tools from '@/components/mixins/Tools';

export default {
  name: 'WaterRecords',
  mixins: [Tools],
  computed: {
    waters() {
      return this.$store.state.waters;
    },
  },
  data() {
    return {
      addWaterForm: {
        date: '',
        size: '',
      },
    };
  },
  methods: {
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
    addWater(payload) {
      const path = 'http://localhost:8000/water';
      axios.post(path, payload)
        .then(() => {
          this.$store.dispatch('getWaters');
          this.$store.dispatch('getCurrent');
          this.$store.dispatch('getCurrentGoal');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addWaterModal.hide();
      this.initForm();
    },
    onDeleteWater(water) {
      this.removeWater(water.id);
    },
    removeWater(waterID) {
      const path = `http://localhost:8000/water/${waterID}`;
      axios.delete(path)
        .then(() => {
          this.$store.dispatch('getWaters');
          this.$store.dispatch('getCurrent');
          this.$store.dispatch('getCurrentGoal');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>
