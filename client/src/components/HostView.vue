<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Host Scans</h1>
        <hr><br><br>
        <router-link :to="{ name: 'home' }" type="button" class="btn btn-success btn-sm">Back to list</router-link>
        <br><br>
        <h1>{{ host }}:{{ port }}</h1>

        <DataTable :data="scans" :columns="columns" class="table table-hover display nowrap" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';
import DataTable from 'datatables.net-vue3'
import DataTablesCore from 'datatables.net-bs5';
import 'datatables.net-responsive';
import 'datatables.net-select';

DataTablesCore.use(bootstrap);
DataTable.use(DataTablesCore);

export default {
  name: 'HostView',
  components: { DataTable },
  data() {
    return {
      host: this.$route.params.host,
      port: this.$route.params.port,
      scans: [],
      columns: [
        { title: 'Scan Date', data: 'date' },
        { title: 'SSLv2', data: 'sslv2' },
        { title: 'SSLv3', data: 'sslv3' },
        { title: 'TLS 1.0', data: 'tls1_0' },
        { title: 'TLS 1.1', data: 'tls1_1' },
        { title: 'TLS 1.2', data: 'tls1_2' },
        { title: 'TLS 1.3', data: 'tls1_3' },
        {
          title: 'Certificate Serial Number', data: 'certificate_serial_number',
          render: function (data, type, row, meta) {
            if (type === 'display') {
              data = '<a class="btn btn-primary" href="/certificate/' + data + '">' + data + '</a>';
            }
            return data;
          }
        },
        { title: 'Weak Algorithm', data: 'weak_algo' },
      ],
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
