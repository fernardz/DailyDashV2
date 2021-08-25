import axios from 'axios';
import Vuex from 'vuex';
import Vue from 'vue';
import moment from 'moment';

/* eslint no-shadow: ["error", { "allow": ["state"] }] */

Vue.use(Vuex);

function getCurrentDate() {
  return moment().format('YYYY-MM-DD');
}

const state = {
  current_water: 0,
  water_goal: 0,
  waters: [],
  vitamin_summary: [],
  vitamins: [],
  tasks_day: [],
  tasks: [],
  task_records: [],
};

const getters = {
// eslint-disable-next-line
  getTaskRecordsById: (state) => (id) => {
    // eslint-disable-next-line
    return state.task_records.filter(task_record => task_record.task_id === id);
  },
};

const actions = {
  getCurrent({ commit }) {
    const path = `http://192.168.1.181:8000/water/get_day_results/${getCurrentDate()}`;
    axios.get(path)
      .then((res) => {
        commit('SET_CURRENT_WATER', res.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
  getWaters({ commit }) {
    const path = 'http://192.168.1.181:8000/water';
    axios.get(path)
      .then((res) => {
        commit('SET_WATERS', res.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
  getCurrentGoal({ commit }) {
    const path = 'http://192.168.1.181:8000/water_goal/current/';
    axios.get(path)
      .then((res) => {
        commit('SET_WATER_GOAL', res.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
  // vitamin calls

  getCurrentVitamins({ commit }) {
    const path = `http://192.168.1.181:8000/vitamins/summary/${getCurrentDate()}`;
    axios.get(path)
      .then((res) => {
        commit('SET_VIT_SUMM', res.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
  getVitamins({ commit }) {
    const path = 'http://192.168.1.181:8000/vitamins/';
    axios.get(path)
      .then((res) => {
        commit('SET_VITS', res.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },

  // task calls
  getDailyTasks({ commit }) {
    const path = `http://192.168.1.181:8000/task_record/day/${getCurrentDate()}`;
    axios.get(path)
      .then((res) => {
        commit('SET_TASK_DAY', res.data);
      })
      .catch((error) => {
      // eslint-disable-next-line
      console.error(error);
      });
  },
  getTasks({ commit }) {
    const path = 'http://192.168.1.181:8000/task';
    axios.get(path)
      .then((res) => {
        commit('SET_TASKS', res.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
  getTaskRecords({ commit }) {
    const path = 'http://192.168.1.181:8000/task_record';
    axios.get(path)
      .then((res) => {
        commit('SET_TASK_RECORDS', res.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
};

const mutations = {
  SET_CURRENT_WATER(state, CurrentWater) {
    state.current_water = CurrentWater;
  },
  SET_WATER_GOAL(state, Goal) {
    state.water_goal = Goal;
  },
  SET_WATERS(state, Waters) {
    state.waters = Waters;
  },
  SET_VIT_SUMM(state, VSumm) {
    state.vitamin_summary = VSumm;
  },
  SET_VITS(state, Vits) {
    state.vitamins = Vits;
  },
  SET_TASK_DAY(state, TDay) {
    state.tasks_day = TDay;
  },
  SET_TASKS(state, Tasks) {
    state.tasks = Tasks;
  },
  SET_TASK_RECORDS(state, taskRecords) {
    state.task_records = taskRecords;
  },
};

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
});
