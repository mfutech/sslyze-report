<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';
import jszip from 'jszip';
import DataTable from 'datatables.net-vue3'
import DataTablesCore from 'datatables.net-bs5';
import 'datatables.net-responsive';
import 'datatables.net-select';
import 'datatables.net-buttons-bs5';
import MenuHeader from '../components/MenuHeader.vue';


DataTablesCore.use(bootstrap);
DataTablesCore.Buttons.jszip(jszip);
DataTable.use(DataTablesCore);

console.log('DataTablesCore:', DataTablesCore);

export default {
  components: {
    DataTable,
    MenuHeader,
  },
  data() {
    return {
      certificates_list: [],
      options: {
        responsive: true,
        select: true,
        layout: {
          topStart: {
            buttons: ['copy', 'csv', 'excel', 'pdf', 'print']
          }
        },
      },
      columns: [
        { title: 'Date', data: 'date' },
        { title: 'Not After', data: 'not_after' },
        { title: 'Not Before', data: 'not_before' },
        { title: 'Public Key Type', data: 'public_key_type' },
        {
          // eslint-disable-next-line no-unused-vars
          title: 'Fingerprint', data: 'fingerprint', "render": function (data, type, _row, meta) {
            if (type === 'display') {
              let data_display = data.substring(0, 10) + '...' + data.substring(data.length - 10);
              data = '<a class="btn btn-primary" href="/certificate/' + data + '">' + data_display + '</a>';
            }
            return data;
          }
        },
        { title: 'Subject', data: 'subject' },
        { title: 'Usage', data: 'nb_host' },
      ],
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


<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <MenuHeader title="Certificate List" />

        <DataTable :columns="columns" :options="options" :data="certificates_list"
          class="table table-hover display nowrap" />

      </div>
    </div>
  </div>
</template>
