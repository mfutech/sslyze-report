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
  name: 'CompHostsList',
  components: {
    DataTable,
  },
  props: ["hosts"],
  data() {
    return {
      options: {
        responsive: true,
        select: true,
        length: 500,
        lengthMenu: [10, 25, 50, { label: 'All', value: -1 }]
      },
      columns: [
        { title: 'Date', data: 'date' },
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
            result = '<span>' + (data.enabled ? 'SSLv2' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'SSLv3', data: 'sslv3', render: function (data, type, row, meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'SSLv3' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'TLS 1.0', data: 'tls1_0', render: function (data, type, row, meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'TLS1.0' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'TLS 1.1', data: 'tls1_1', render: function (data, type, row, meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'TLS1.1' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'TLS 1.2', data: 'tls1_2', render: function (data, type, row, meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'TLS1.2' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'TLS 1.3', data: 'tls1_3', render: function (data, type, row, meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'TLS1.3' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'Old', data: 'moz_old', render: function (data, type, row, meta) {
            let result = (data.compliant ? 'Old Compliant' : 'Old Non Compliant');
            if (type === 'display') {
              let res_class = "border border-2 " + (data.compliant ? 'border-success' : 'border-danger');
              result = '<button class="' + res_class + '">' + result + '</button>';
            }
            return result;
          }
        },
        {
          title: 'Intermediate', data: 'moz_intermediate', render: function (data, type, row, meta) {
            let result = (data.compliant ? 'Intermediate Compliant' : 'Intermediate Non Compliant');
            if (type === 'display') {
              let res_class = "border border-2 " + (data.compliant ? 'border-success' : 'border-danger');
              result = '<button class="' + res_class + '">' + result + '</button>';
            }
            return result;
          }
        },
        {
          title: 'Modern', data: 'moz_modern', render: function (data, type, row, meta) {
            let result = (data.compliant ? 'Modern Compliant' : 'Modern Non Compliant');
            if (type === 'display') {
              let res_class = "border border-2 " + (data.compliant ? 'border-success' : 'border-danger');
              result = '<button class="' + res_class + '">' + result + '</button>';
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

};
</script>


<template>

  <DataTable :columns="columns" :options="options" :data="hosts" class="table table-hover display nowrap" />

</template>
