<template>
  <div class="container">
    <div class="columns is-mobile">
      <div class="column has-text-centered">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/168px-Spotify_logo_without_text.svg.png">
        <div class="search">
          <input class="input is-primary" type="text" placeholder="Enter artist name" v-model="searchTerm">
          <button class="button is-success" @click="redirectToSearchPage">Strart Quiz</button>
          <p class="size-is-7 is-italic">Please be aware that some artist may not be available due to lack of "preview" tracks on Spotify</p>
        </div>
      </div>
    </div>
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
      const encodedSearchTerm = encodeURIComponent(this.searchTerm);
      this.$router.push({ path: `/${encodedSearchTerm}` });
    }
  }
};
</script>

<style scoped>

.search {
  margin: 1rem;
}

.input {
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.size-is-7 {
  margin: 1rem;
}

</style>
