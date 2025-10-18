<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Host Scans</h1>
        <hr><br><br>
        <router-link :to="{ name: 'home' }" type="button" class="btn btn-success btn-sm">Back to list</router-link>
        <br><br>
        <h1>{{ host }}:{{ port }}</h1>

        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Scan Date</th>
              <th scope="col">SSLv2</th>
              <th scope="col">SSLv3</th>
              <th scope="col">TLS 1.0</th>
              <th scope="col">TLS 1.1</th>
              <th scope="col">TLS 1.2</th>
              <th scope="col">TLS 1.3</th>
              <th scope="col">Certificate Serial Number</th>
              <th scope="col">Weak Algorithm</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(scan, index) in scans" :key="index">
              <td>{{ scan.date }}</td>
              <td>{{ scan.sslv2 }}</td>
              <td>{{ scan.sslv3 }}</td>
              <td>{{ scan.tls1_0 }}</td>
              <td>{{ scan.tls1_1 }}</td>
              <td>{{ scan.tls1_2 }}</td>
              <td>{{ scan.tls1_3 }}</td>
              <td>
                <router-link
                  :to="{ name: 'certificateview', params: { cert_serial: scan.certificate_serial_number } }">{{
                    scan.certificate_serial_number }}</router-link>

              </td>
              <td>{{ scan.weak_algo }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'HostView',
  data() {
    return {
      host: this.$route.params.host,
      port: this.$route.params.port,
      scans: [],
    };
  },
  methods: {
    fetchHostDetails() {
      const path = '/api/host/' + this.host + '/' + this.port;
      axios.get(path)
        .then((response) => {
          if (response.data.status === 'success') {
            this.scans = response.data.scans;
            this.host = response.data.host;
            this.port = response.data.port;
          } else {
            console.error('Failed to fetch host details');
          }
        })
        .catch((error) => {
          console.error('Error fetching host details:', error);
        });
    },
  },
  created() {
    this.fetchHostDetails();
  },
};
</script>
