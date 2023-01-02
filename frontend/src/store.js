import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    refCount: 0,
    isLoading: false
  },
  mutations: {
    loading(state, isLoading) {
      console.log({isLoading})
      if (isLoading) {
        state.refCount++;
        state.isLoading = true;
      } else if (state.refCount > 0) {
        state.refCount--;
        state.isLoading = (state.refCount > 0);
      }
    }
  }
})