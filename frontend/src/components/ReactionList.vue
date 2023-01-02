<template>
  <div>
    <div v-for="(v, index) in value" v-bind:key="index" class="user-list">
      <div v-if="index === 0" class="reaction">{{title}}</div>
      <span class="username">{{ v.username }} - </span>
      <span v-for="(em, index) in v.emoji_infos" v-bind:key="index" class="emoji">
        {{ convertStrToEmoji(em.emoji) }}: {{ em.count}}
      </span><br/>
    </div>
  </div>
</template>

<script>
export default {
  name: "reactionList",
  data: function () {
    return {
      value: 0
    };
  },
  props: ["title"],
  methods: {
    setValue: function(value) {
        this.value = value;
    },
    // 사용하는 이모지에 따라서 커스텀
    convertStrToEmoji: function (emojiType) {
      switch (emojiType) {
        case '기도':
        case 'pray':
          return '🙏'
        case 'heart':
          return '❤️'
        case '+1':
          return '👍'
        default:
          return '💖'
      }
    }
  }
}
</script>

<style scoped>
  @import "../assets/styles/reactionList.css";
</style>