<template>
 <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Certificates</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Book</button>
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
                <th scope="col">sslv2</th>
                <th scope="col">sslv3</th>
                <th scope="col">tls1_0</th>
                <th scope="col">tls1_1</th>
                <th scope="col">tls1_2</th>
                <th scope="col">tls1_3</th>
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
              <td>{{ cert.sslv2 }}</td>
              <td>{{ cert.sslv3 }}</td>
              <td>{{ cert.tls1_0 }}</td>
              <td>{{ cert.tls1_1 }}</td>
              <td>{{ cert.tls1_2 }}</td>
              <td>{{ cert.tls1_3 }}</td>
              <td>{{ cert.not_after }}</td>
              <td>{{ cert.weak_algo }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
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
  name: 'Certificates',
  data() {
    return {
      certificates: [],
    };
  },
  methods: {
    fetchCertificates() {
      const path = 'http://localhost:5000/certificates';
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

