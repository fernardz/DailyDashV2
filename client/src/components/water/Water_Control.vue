<template>
<div>
    <b-button pill variant="outline-info" class="w-25" @click="onSubmitQuick(8)">8</b-button>
    <b-button pill variant="outline-info" class="w-25"  @click="onSubmitQuick(16)">16</b-button>
    <b-button pill variant="outline-info" class="w-25"  @click="onSubmitQuick(32)">32</b-button>
    <b-button pill variant="outline-info" class="w-25"  v-b-modal.water-modal>+</b-button>
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
import Tools from '@/components/mixins/Tools';

export default {
  name: 'WaterControl',
  mixins: [Tools],
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
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addWaterModal.hide();
      this.initForm();
    },
    onSubmitQuick(amount) {
      const payload = {
        date: this.getCurrentDate(),
        size: amount,
      };
      this.addWater(payload);
      this.initForm();
    },
    addWater(payload) {
      const path = 'http://rasp-srv:8000/water';
      axios.post(path, payload)
        .then(() => {
          this.$emit('clicked', true);
          this.$store.dispatch('getWaters');
          this.$store.dispatch('getCurrent');
          this.$store.dispatch('getCurrentGoal');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
  },
};
</script>
