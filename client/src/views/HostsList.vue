<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';

import HostsList from '../components/HostsList.vue';
import MenuHeader from '../components/MenuHeader.vue';


export default {
  components: {
    HostsList,
    MenuHeader,
  },

  data() {
    return {
      hosts: [],

    };
  },
  methods: {
    fetchHosts_list() {
      console.log('Fetching hosts_list from /api/hosts');
      const path = '/api/hosts';
      axios.get(path)
        .then((response) => {
          if (response.data.status === 'success') {
            this.hosts = response.data.hosts;
            console.log('Hosts list fetched:', response);
          } else {
            console.error('Failed to fetch hosts list');
          }
        })
        .catch((error) => {
          console.error('Error fetching hosts list:', error);
        });
    },
  },
  created() {
    this.fetchHosts_list();
  },
  watch: {
    hosts(val, oldVal) {
      console.log('hosts list changed (watch):', val && val.length, 'old:', oldVal && oldVal.length);
    },
  },
};
</script>


<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <MenuHeader title="Hosts List" />

        <HostsList :hosts="hosts" />

      </div>
    </div>
  </div>
</template>
