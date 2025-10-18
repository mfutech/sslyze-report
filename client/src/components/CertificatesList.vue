<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Certificates_list</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Book</button>
        <a href="/Ping" type="button" class="btn btn-primary btn-sm">Ping</a>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">date</th>
              <th scope="col">serial_number</th>
              <th scope="col">subject</th>
              <th scope="col">public_key_type</th>
              <th scope="col">not_after</th>
              <th scope="col">weak_algo</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(cert, i) in certificates_list" :key="cert.serial_number || 'cert-' + i">
              <td>{{ cert.date }}</td>

              <td>{{ cert.serial_number }}</td>
              <td>{{ cert.subject }}</td>
              <td>{{ cert.public_key_type }}</td>
              <td>{{ cert.not_after }}</td>
              <td>{{ cert.weak_algo }}</td>
              <td>
                <div class="btn-group" role="group">
                  <router-link class="btn btn-primary"
                    :to="{ name: 'certificateview', params: { cert_serial: cert.serial_number } }">View</router-link>
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
  name: 'Certificates_listList',
  data() {
    return {
      certificates_list: [],
      others: [{ name: 'a' }, { name: 'b' }, { name: 'c' }],
    };
  },
  methods: {
    fetchCertificates_list() {
      console.log('Fetching certificates_list from /api/certificates');
      const path = '/api/certificates';
      axios.get(path)
        .then((response) => {
          if (response.data.status === 'success') {
            this.certificates_list = response.data.certificates;
            console.log('Certificates_list fetched:', response);
          } else {
            console.error('Failed to fetch certificates_list');
          }
        })
        .catch((error) => {
          console.error('Error fetching certificates_list:', error);
        });
    },
  },
  created() {
    this.fetchCertificates_list();
  },
  watch: {
    certificates_list(val, oldVal) {
      console.log('certificates_list changed (watch):', val && val.length, 'old:', oldVal && oldVal.length);
    },
  },
};
</script>
