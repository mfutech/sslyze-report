<script>

/*eslint no-unused-vars: ["error", { "varsIgnorePattern": "^_" }]*/

import axios from 'axios';
import * as bootstrap from 'bootstrap';
import jszip from 'jszip';
import DataTable from 'datatables.net-vue3'
import DataTablesCore from 'datatables.net-bs5';
import Buttons from 'datatables.net-buttons-bs5';
import 'datatables.net-buttons/js/buttons.html5.mjs';
import 'datatables.net-searchpanes-bs5';
 


window.JSZip = jszip; // or globalThis.JSZip = JSZip;

DataTablesCore.use(bootstrap);
Buttons.use(bootstrap);
DataTablesCore.use(Buttons);
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
        length: 100,
        lengthMenu: [10, 25, 50, 100, { label: 'All', value: -1 }],
        layout: {
          topStart: {
            buttons: ['copy', 'csv', 'excel', 'pdf', 'print']
          }
        },
      },
      columns: [
        { title: 'Date', data: 'date' },
        {
          title: 'Host', data: 'host',
          render: function (data, type, row, __meta) {
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
          title: 'SSLv2', data: 'sslv2', render: function (data, __type, __row, __meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'SSLv2' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'SSLv3', data: 'sslv3', render: function (data, __type, __row, __meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'SSLv3' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'TLS 1.0', data: 'tls1_0', render: function (data, __type, __row, __meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'TLS1.0' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'TLS 1.1', data: 'tls1_1', render: function (data, __type, __row, __meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'TLS1.1' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'TLS 1.2', data: 'tls1_2', render: function (data, __type, __row, __meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'TLS1.2' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'TLS 1.3', data: 'tls1_3', render: function (data, __type, __row, __meta) {
            let result = data
            result = '<span>' + (data.enabled ? 'TLS1.3' : '-') + '</span>';
            return result;
          }
        },
        {
          title: 'Old', data: 'moz_old', render: function (data, type, __row, __meta) {
            let result = (data.compliant ? 'Old Compliant' : 'Old Non Compliant');
            if (type === 'display') {
              let res_class = "border border-2 " + (data.compliant ? 'border-success' : 'border-danger');
              result = '<button class="' + res_class + '">' + result + '</button>';
            }
            return result;
          }
        },
        {
          title: 'Intermediate', data: 'moz_intermediate', render: function (data, type, __row, __meta) {
            let result = (data.compliant ? 'Intermediate Compliant' : 'Intermediate Non Compliant');
            if (type === 'display') {
              let res_class = "border border-2 " + (data.compliant ? 'border-success' : 'border-danger');
              result = '<button class="' + res_class + '">' + result + '</button>';
            }
            return result;
          }
        },
        {
          title: 'Modern', data: 'moz_modern', render: function (data, type, __row, __meta) {
            let result = (data.compliant ? 'Modern Compliant' : 'Modern Non Compliant');
            if (type === 'display') {
              let res_class = "border border-2 " + (data.compliant ? 'border-success' : 'border-danger');
              result = '<button class="' + res_class + '">' + result + '</button>';
            }
            return result;
          }
        },
        {
          title: 'Fingerprint', data: 'certificate_fingerprint', "render": function (data, type, __row, __meta) {
            if (type === 'display') {
              let output = data.map(function (fingerprint) {
                let fingerprint_disp = fingerprint.length > 18 ? fingerprint.substr(0, 15) + '...' : fingerprint;
                return '<a class="btn btn-primary" href="/certificate/' + fingerprint + '">' + fingerprint_disp + '</a><br>';
              });
              return output;
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
