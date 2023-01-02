<script src="main.js"></script>
<template>
  <div id="app">
    <header>
      <img src="./assets/logos/heymoji-logo.png" width="250">
    </header>

    <div v-if="isLoading">
      <div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>
    </div>
    <UserList msg="Welcome to Your Vue.js App"/>

    <footer>
      🏃‍♂️모두가 함께 앞으로 나아가면 성공은 저절로 따라옵니다🏃‍♀️
    </footer>
  </div>
</template>
<script>

import UserList from './components/UserList.vue'
import { mapState } from 'vuex';

export default {
  name: 'App',
  components: {
    UserList
  },
  computed: {
    ...mapState(['isLoading', 'refCount'])
  },
  created() {
    this.axios.interceptors.request.use((config) => {
      this.$store.commit('loading', true);
      return config;
    }, (error) => {
      this.$store.commit('loading', false);
      return Promise.reject(error);
    });

    this.axios.interceptors.response.use((response) => {
      this.$store.commit('loading', false);
      return response;
    }, (error) => {
      this.$store.commit('loading', false);
      return Promise.reject(error);
    });
  }
}
</script>

<style>
@import url('https://cdn.rawgit.com/innks/NanumSquareRound/master/nanumsquareround.min.css');
@import "../src/assets/styles/main.css";
</style>
