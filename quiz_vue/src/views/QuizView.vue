<template>
  <div class="container">
    <div class="columns is-mobile is-centered">
    <div class="column has-text-centered">
    <p class="is-size-2">{{ artistData.artist_name }}</p>
    <figure class="image is-64x64 is-inline-block">
      <img v-bind:src="artistData.artist_picture" class="is-rounded">
    </figure>
    <p v-for="item, index in questionList">
    
      <div v-if="index === currentIndex">
      <div class="box">
      <p class="is-size-3">Song #{{ index+1 }}</p>
      <p v-for="song in item.slice(3)">
        <div>
          <audio controls autoplay>
            <source :src="song.sample" type="audio/mpeg">
          </audio>
        </div>
      </p>
        <p v-for="song in item.slice(0,3)">
          <div class="buttons is-centered">
            <button class="button is-primary is-medium is-inline-block {'active': isActive}" @click="checkAnswer(song.title, index)">
            {{ song.title }}
            </button>
          </div>
        </p>
      </div>
      </div>
    </p>
    <div v-if="currentIndex === 3">
        <figure class="image is-inline-block">
          <img src="https://s3.amazonaws.com/heights-photos/wp-content/uploads/2020/10/05200825/thumbs-up-01.png" class="is-rounded">
        </figure>
          <p class="is-size-3 is-relative">Congrats, you scored: {{ points }}/{{ questionList.length }} points</p>
      </div>
      <div class="box points" :class="{ 'animate': isAnimated }">
            <p class="is-size-4 is-relative">You have: {{ points }}/{{ questionList.length }}  points</p>
            <p v-if="this.points >= 3" class="is-size-4 is-relative">{{ congratsMessage }}</p>
            <button @click="refreshButton()">New Quiz</button>
      </div>
    </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
  name: 'Quiz',
  data() {
        return {
            artistData: [],
            questionList: [],
            answers: {},
            isActive: true,
            points: 0,
            tries: 0,
            currentIndex: 0,
            isAnimated: false,
            congratsMessage: 'Congrats, you the best!'
        }
    },
  mounted() {
        this.getData()
    },
  watch: {
    points (newPoints) {
      this.points = Math.min(newPoints, 3)
    }
  },
  methods: {
        async getData() {

            const artist = this.$route.params.artist

            await axios
                .get(`/questions/${artist}`)
                .then(response => {
                    this.artistData = response.data
                    this.questionList = this.artistData.questions
                    this.answers.ans1 = this.questionList[0][3].title
                    this.answers.ans2 = this.questionList[1][3].title
                    this.answers.ans3 = this.questionList[2][3].title
                })
                .catch(error => {
                    console.log(error)
                    toast({
                        message: 'Please pick different artist',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 5000,
                        position: 'top-left',
                    })
                })
        },
        refreshButton() {
          console.log('Refreshed')
          location.reload();
        },
        nextQuestion() {
          this.currentIndex += 1;
        },
        toggleAnimation() {
          this.isAnimated = !this.isAnimated;
          setTimeout(() => {
            this.isAnimated = false;
          }, 500);
        },
        checkAnswer(text, index) {
          this.nextQuestion()
          this.tries += 1;
          console.log(this.tries)
          if (index == 0) {
            if (text == this.answers.ans1) {
              console.log(this.answers.ans1)
              this.points += 1
              this.toggleAnimation()
              toast({
                        message: 'Good answer!',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 1000,
                        position: 'bottom-right',
                    })
            }
            else {
            console.log(this.ans1)
            toast({
                      message: 'Wrong answer!',
                      type: 'is-danger',
                      dismissible: true,
                      pauseOnHover: true,
                      duration: 1000,
                      position: 'bottom-right',
                  })
          }
          }
          else if (index == 1) {
            if (text == this.answers.ans2) {
              console.log(this.answers.ans2)
              this.points += 1
              this.toggleAnimation()
              toast({
                        message: 'Good answer!',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 1000,
                        position: 'bottom-right',
                    })
            }
            else {
            console.log(this.ans1)
            toast({
                      message: 'Wrong answer!',
                      type: 'is-danger',
                      dismissible: true,
                      pauseOnHover: true,
                      duration: 1000,
                      position: 'bottom-right',
                  })
          }
          }
          else if (index == 2) {
            if (text == this.answers.ans3) {
              console.log(this.answers.ans3)
              this.points += 1
              this.toggleAnimation()
              toast({
                        message: 'Good answer!',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 1000,
                        position: 'bottom-right',
                    })
            }
            else {
            console.log(this.ans1)
            toast({
                      message: 'Wrong answer!',
                      type: 'is-danger',
                      dismissible: true,
                      pauseOnHover: true,
                      duration: 1000,
                      position: 'bottom-right',
                  })
          }
          }
  },
  },
}  
</script>

<style scoped>
.buttons{
  margin: 1rem;
}

.box {
  animation-fill-mode: both;
  margin-top: 1rem;
}

.points {
  background-color: green;
  color: white;
}

.animate {
  animation: bounce 0.5s ease-in-out;
}

@keyframes bounce {
  0% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0); }
}
</style>