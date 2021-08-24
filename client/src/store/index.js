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
};

const getters = {};

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
};

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
});
