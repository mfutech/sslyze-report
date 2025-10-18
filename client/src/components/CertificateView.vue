<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Certificate Details</h1>
        <hr><br><br>
        <h1>{{ certificate.subject }}</h1>
        <h2>Scan Results</h2>
        <table class="table table-hover">
          <tr>
            <th>Scan date</th>
            <td>{{ certificate.date }}</td>
          </tr>
          <tr>
            <th>Serial Number</th>
            <td>{{ certificate.serial_number }}</td>
          </tr>
          <tr>
            <th>Subject</th>
            <td>{{ certificate.subject }}</td>
          </tr>
          <tr>
            <th>Public Key Type</th>
            <td>{{ certificate.public_key_type }}</td>
          </tr>
          <tr>
            <th>Not After</th>
            <td>{{ certificate.not_after }}</td>
          </tr>
          <tr>
            <th>Weak Algorithm</th>
            <td>{{ certificate.weak_algo }}</td>
          </tr>
        </table>

        <h2>hosts</h2>

        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Host</th>
              <th scope="col">SSLv2</th>
              <th scope="col">SSLv3</th>
              <th scope="col">TLS 1.0</th>
              <th scope="col">TLS 1.1</th>
              <th scope="col">TLS 1.2</th>
              <th scope="col">TLS 1.3</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(host, index) in hosts" :key="index">
              <td>{{ host.host }}:{{ host.port }}</td>
              <td>{{ host.sslv2 }}</td>
              <td>{{ host.sslv3 }}</td>
              <td>{{ host.tls1_0 }}</td>
              <td>{{ host.tls1_1 }}</td>
              <td>{{ host.tls1_2 }}</td>
              <td>{{ host.tls1_3 }}</td>
              <td>{{ host.weak_algo }}</td>
              <td>
                <div class="btn-group" role="group">
                  <router-link class="btn btn-primary"
                    :to="{ name: 'hostview', params: { host: host.host, port: host.port } }">View</router-link>
                </div>
              </td>
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
  name: 'CertificateView',
  data() {
    return {
      cert_serial: this.$route.params.cert_serial,
      certificate: {},
      hosts: []
    };
  },
  methods: {
    fetchCertificateDetails() {
      const path = '/api/certificate/' + this.cert_serial;
      axios.get(path)
        .then((response) => {
          if (response.data.status === 'success') {
            this.certificate = response.data.certificate;
            this.hosts = response.data.hosts;
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
    this.fetchCertificateDetails();
  },
};
</script>
