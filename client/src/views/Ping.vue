<template>
  <div>
    <MenuHeader title="Ping Page" />
    <p>status : <button type="button" class="btn btn-primary">{{ msg }}</button></p>
  </div>
</template>

<script>
import MenuHeader from '@/components/MenuHeader.vue';
import axios from 'axios';

export default {
  name: 'PingPage',
  components: { MenuHeader },
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {

          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
