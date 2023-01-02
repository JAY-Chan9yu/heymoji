<script src="../main.js"></script>
<template>
  <div>
    <div class="table-title">
      <h3>
        <span
            v-for="(t, index) in title"
            :key="index"
            class="item"
            :style="{animationDelay: index*100+'ms'}"
            v-text="t"
        />
      </h3>
    </div>

    <div class="table-title" style="display: inline-block;">
      <div class="filter">
        <v-text-field solo v-model="year" rounded placeholder="year"></v-text-field>
      </div>
      <div class="filter">
        <v-text-field solo v-model="month" rounded placeholder="month"></v-text-field>
      </div>
      <div class="filter__department">
        <v-text-field solo v-model="department" rounded placeholder="부서"></v-text-field>
      </div>
      <v-btn rounded v-on:click="getMemberList(year, month, department)" color="rgb(189, 128, 74)"
             style="color: white; font-weight: bolder">
        가져오기
      </v-btn>
    </div>

    <div>💡이름 옆 숫자는 동료에게 받은 모든 Emoji 합계입니다.</div>

    <div v-if="hasResult" class="container">
      <div v-for="(user, index) in users" v-bind:key="user.id" class="content"
           v-on:click="getReactionList(user.id, year, month)">
        <div class="content__index">
          <span>{{ index + 1 }}.</span>
        </div>
        <div class="content__user">
          <img class="avatar" v-if="user.avatar_url" :src="user.avatar_url">
          <img class="avatar" v-else src="../assets/logos/heymoji.png">
          {{ user.username }}
          <span class="department" v-if="user.department">{{ user.department }}</span>
        </div>
        <div class="content__get"><span class="received_reaction">🤩 + {{ user.received_reaction_count }}</span></div>
        <reaction-list data-active="false" :ref="'reaction-' + user.id" :title=reactionTitle
                       style="display: block"></reaction-list>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ReactionList from "./ReactionList";

export default {
  name: 'UserList',
  components: {
    'reaction-list': ReactionList
  },
  data: function () {
    let date = new Date();

    return {
      title: "✨최고의 동료가 최고의 복지다✨",
      reactionTitle: "리액션한 크루 리스트",
      baseURI: "http://127.0.0.1:8000",
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,OPTIONS'
      },
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      department: null,
      users: []
    }
  },
  computed: {
    hasResult: function () {
      return this.users.length > 0
    },
  },
  methods: {
    getMemberList: function (year, month, department) {
      if (year === '') year = null
      if (month === '') month = null
      if (department === '') department = null

      let config = {
        headers: this.headers,
        params: {'year': year, 'month': month, 'department': department},
      }
      axios.get(`${this.baseURI}/users/`, config)
          .then((result) => {
            this.users = result.data
          })
    },
    getReactionList: function (userId, year, month) {
      if (year === '') year = null
      if (month === '') month = null

      let config = {
        headers: this.headers,
        params: {'year': year, 'month': month},
      }
      let isActive = this.$refs['reaction-' + userId][0].$attrs['data-active'];

      if (isActive === 'false') {
        // 리액션한 크루들의 리스트를 보여준다.
        axios.get(`${this.baseURI}/users/${userId}/reactions/`, config)
            .then((result) => {
              this.$refs['reaction-' + userId][0].setValue(result.data)
              this.$refs['reaction-' + userId][0].$attrs['data-active'] = "true"
            })
      } else {
        this.$refs['reaction-' + userId][0].$attrs['data-active'] = "false"
        this.$refs['reaction-' + userId][0].setValue([])
      }
    },
  },
  mounted() {
    this.getMemberList(this.year, this.month);
  }
}
</script>

<style>
  @import "../assets/styles/userList.css";
</style>