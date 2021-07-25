import moment from 'moment';

export default {
  methods: {
    getCurrentDate() {
      return moment().format('YYYY-MM-DD');
    },
  },
};
