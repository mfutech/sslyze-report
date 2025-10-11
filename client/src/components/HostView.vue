<template>
 <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Certificates</h1>
        <hr><br><br>
        <router-link :to="{ name: 'home' }" type="button" class="btn btn-success btn-sm">Back to list</router-link>
        <br><br>
        <h1>{{  host  }}:{{ port }}</h1>
        <ul>
          <li>Host: {{ host }}</li>
          <li>Port: {{ port }}</li>
          <li>Scan Started: {{ scan_started }}</li>
          <li>Scan Completed: {{ scan_completed }}</li>
          <li>Scan ID: {{ scan_id }}</li>
        </ul>
        <h2>connectivity result</h2>
        <ul>
          <li>highest_tls_version_supported: {{ scan_results.connectivity_result.highest_tls_version_supported }}</li>
          <li>cipher_suite_supported: {{ scan_results.connectivity_result.cipher_suite_supported }}</li>
          <li>client_auth_requirement: {{ scan_results.connectivity_result.client_auth_requirement }}</li>
          <li>supports_ecdh_key_exchange: {{ scan_results.connectivity_result.supports_ecdh_key_exchange }}</li>
        </ul>
 
        <h2>Scan Results</h2>
        <pre>{{ scan_results }}</pre>

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
      date: "",
      scan_started: "",
      scan_completed: "",
      json: {},
      scan_id: "",
      hostDetails: {},
      scan_results: {},
    };
  },
  methods: {
    fetchHostDetails(cert_id) {
      const path = '/api/host/' + this.host + '/' + this.port;
      axios.get(path)
        .then((response) => {
          if (response.data.status === 'success') {
            this.hostDetails = response.data.hostDetails;
            this.host = response.data.hostDetails.host;
            this.port = response.data.hostDetails.port;
            this.date = response.data.hostDetails.date;
            this.scan_started = response.data.hostDetails.scan_started;
            this.scan_completed = response.data.hostDetails.scan_completed;
            this.scan_id = response.data.hostDetails.scan_id;
            this.json = JSON.parse(response.data.hostDetails.scan_result_json);
            this.scan_results = this.json.server_scan_results[0];
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

