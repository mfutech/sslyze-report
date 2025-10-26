<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';
import DataTable from 'datatables.net-vue3'
import DataTablesCore from 'datatables.net-bs5';
import 'datatables.net-responsive';
import 'datatables.net-select';


DataTablesCore.use(bootstrap);
DataTable.use(DataTablesCore);

console.log('DataTablesCore:', DataTablesCore);

export default {
  name: 'HostsList',
  components: {
    DataTable,
  },
  data() {
    return {
      hosts: [],
      options: {
        responsive: true,
        select: true,
      },
      columns: [
        { title: 'Date', data: 'last_scan' },
        {
          title: 'Host', data: 'host',
          render: function (data, type, row, meta) {
            if (type === 'display') {
              data = '<a href="/host/' + data + '/' + row.port + '" class="btn btn-primary">' + data + ':' + row.port + '</a>';
            }
            // console.log('Rendering host column:', data, type, row, meta);
            return data;
          }
        },
        // {
        //   title: 'Host', data: 'host', render: function (data, type, row, meta) {
        //     if (type === 'display') {
        //       data = data + ':' + row.port;
        //     }
        //     return data;
        //   }
        // },
        {
          title: 'SSLv2', data: 'sslv2', render: function (data, type, row, meta) {
            let result = data
            if (type === 'display') {
              result = '<span>' + (data.enabled ? 'Yes' : 'No') + '</span>';
            }
            return result;
          }
        },
        {
          title: 'SSLv3', data: 'sslv3', render: function (data, type, row, meta) {
            let result = data
            if (type === 'display') {
              result = '<span>' + (data.enabled ? 'Yes' : 'No') + '</span>';
            }
            return result;
          }
        },
        {
          title: 'TLS 1.0', data: 'tls1_0', render: function (data, type, row, meta) {
            let result = data
            if (type === 'display') {
              result = '<span>' + (data.enabled ? 'Yes' : 'No') + '</span>';
            }
            return result;
          }
        },
        {
          title: 'TLS 1.1', data: 'tls1_1', render: function (data, type, row, meta) {
            let result = data
            if (type === 'display') {
              result = '<span>' + (data.enabled ? 'Yes' : 'No') + '</span>';
            }
            return result;
          }
        },
        {
          title: 'TLS 1.2', data: 'tls1_2', render: function (data, type, row, meta) {
            let result = data
            if (type === 'display') {
              result = '<span>' + (data.enabled ? 'Yes' : 'No') + '</span>';
            }
            return result;
          }
        },
        {
          title: 'TLS 1.3', data: 'tls1_3', render: function (data, type, row, meta) {
            let result = data
            if (type === 'display') {
              result = '<span>' + (data.enabled ? 'Yes' : 'No') + '</span>';
            }
            return result;
          }
        },
        {
          title: 'Old', data: 'moz_old', render: function (data, type, row, meta) {
            let result = data
            if (type === 'display') {
              result = '<span>' + (data.compliant ? 'Yes' : 'No') + '</span>';
            }
            return result;
          }
        },
        {
          title: 'Intermediate', data: 'moz_intermediate', render: function (data, type, row, meta) {
            let result = data
            if (type === 'display') {
              result = '<span>' + (data.compliant ? 'Yes' : 'No') + '</span>';
            }
            return result;
          }
        },
        {
          title: 'Modern', data: 'moz_modern', render: function (data, type, row, meta) {
            let result = data
            if (type === 'display') {
              result = '<span>' + (data.compliant ? 'Yes' : 'No') + '</span>';
            }
            return result;
          }
        },
        {
          title: 'Serial Number', data: 'certificate_serial_number', "render": function (data, type, row, meta) {
            if (type === 'display') {
              let output = '';
              data.forEach(function (serial) {
                let serial_disp = serial.length > 18 ? serial.substr(0, 15) + '...' : serial;
                output += '<a class="btn btn-primary" href="/certificate/' + serial + '">' + serial_disp + '</a><br>';
              });
              data = output;
            }
            return data;
          }
        },
      ],
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
        <h1>Hosts List</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Book</button>
        <a href="/Ping" type="button" class="btn btn-primary btn-sm">Ping</a>
        <br><br>

        <DataTable :columns="columns" :options="options" :data="hosts" class="table table-hover display nowrap" />

      </div>
    </div>
  </div>
</template>
