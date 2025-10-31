<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <MenuHeader :title="'Certificate Details : ' + certificate.subject" />
        <h2>Scan Results</h2>
        <table class="table table-hover">
          <tbody>
            <tr>
              <th>Scan date</th>
              <td>{{ certificate.date }}</td>
              <th>Subject</th>
              <td>{{ certificate.subject }}</td>
            </tr>
            <tr>
              <th>Serial Number</th>
              <td>{{ certificate.serial_number }}</td>
              <th>Fingerprint</th>
              <td>{{ certificate.fingerprint }}</td>
            </tr>

            <tr>
              <th>Public Key Type</th>
              <td>{{ certificate.public_key_type }}</td>
            </tr>
            <tr>
              <th>Not After</th>
              <td>{{ certificate.not_after }}</td>

              <th>Not Before</th>
              <td>{{ certificate.not_before }}</td>
            </tr>
          </tbody>
        </table>

        <h2>hosts</h2>

        <HostsList :hosts="hosts" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';


import HostsList from '../components/HostsList.vue';
import MenuHeader from '../components/MenuHeader.vue';


export default {
  components: { HostsList, MenuHeader },
  data() {
    return {
      cert_serial: this.$route.params.cert_serial,
      certificate: {},
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
