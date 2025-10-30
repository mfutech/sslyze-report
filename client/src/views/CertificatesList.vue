<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';
import DataTable from 'datatables.net-vue3'
import DataTablesCore from 'datatables.net-bs5';
import 'datatables.net-responsive';
import 'datatables.net-select';
import MenuHeader from '../components/MenuHeader.vue';



DataTablesCore.use(bootstrap);
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
      },
      columns: [
        { title: 'Date', data: 'date' },
        { title: 'Not After', data: 'not_after' },
        { title: 'Public Key Type', data: 'public_key_type' },
        {
          title: 'Serial Number', data: 'serial_number', "render": function (data, type, row, meta) {
            if (type === 'display') {
              data = '<a class="btn btn-primary" href="/certificate/' + data + '">' + data + '</a>';
            }
            return data;
          }
        },
        { title: 'Subject', data: 'subject' },
        { title: 'Weak Algorithm', data: 'weak_algo' },
      ],
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
