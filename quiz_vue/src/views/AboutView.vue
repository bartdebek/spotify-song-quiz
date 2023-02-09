<template>
  <div>
    <input type="text" v-model="searchTerm"/>
    <button @click="redirectToSearchPage">Search</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: ''
    }
  },
  methods: {
    redirectToSearchPage() {
      this.$router.push({ path: `/${this.searchTerm}` });
    }
  }
};
</script>
