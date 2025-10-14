<template>
 <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Certificates</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Book</button>
        <a href="/Ping" type="button" class="btn btn-primary btn-sm">Ping</a>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
                <th scope="col">date</th>
                <th scope="col">hostname</th>
                <th scope="col">port</th>
                <th scope="col">serial_number</th>
                <th scope="col">subject</th>
                <th scope="col">public_key_type</th>
                <th scope="col">not_after</th>
                <th scope="col">weak_algo</th>
                <th></th> 
            </tr>
          </thead>
          <tbody>
            <tr v-for="(cert, index) in certificates" :key="index">
              <td>{{ cert.date }}</td>
              <td>{{ cert.hostname }}</td>
              <td>{{ cert.port }}</td>
              <td>{{ cert.serial_number }}</td>
              <td>{{ cert.subject }}</td>
              <td>{{ cert.public_key_type }}</td>
              <td>{{ cert.not_after }}</td>
              <td>{{ cert.weak_algo }}</td>
              <td>
                <div class="btn-group" role="group">
                  <router-link :to="{ name: 'hostview', params: { host: cert.hostname, port: cert.port }}">View</router-link>
                  <!-- <a href="/certificates/{{ cert.serial_number }}/view" type="button" class="btn btn-warning btn-sm">View</a> -->
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
  name: 'CertificatesList',
  data() {
    return {
      certificates: [],
    };
  },
  methods: {
    fetchCertificates() {
      const path = '/api/certificates';
      axios.get(path)
        .then((response) => {
          if (response.data.status === 'success') {
            this.certificates = response.data.certificates;
          } else {
            console.error('Failed to fetch certificates');
          }
        })
        .catch((error) => {
          console.error('Error fetching certificates:', error);
        });
    },
  },
  created() {
    this.fetchCertificates();
  },
};
</script>

