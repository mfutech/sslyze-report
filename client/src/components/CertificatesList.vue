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
  name: 'CertificatesList',
  components: {
    DataTable,
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
        <h1>Certificates List</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Book</button>
        <a href="/Ping" type="button" class="btn btn-primary btn-sm">Ping</a>
        <br><br>

        <DataTable :columns="columns" :options="options" ajax="http://localhost:8080/api/certificates"
          :data="certificates_list" class="table table-hover display nowrap" />
        <hr>
        <DataTable class="display">
          <thead>
            <tr>
              <th>First</th>
              <th>Second</th>
            </tr>
          </thead>
        </DataTable>
        <hr>
        <DataTable ajax="/api/certificates" class="display">
        </DataTable>
        <hr>
        data table with data prop
        <p>Data table with data prop</p>
        <DataTable :options="options" :data="others" class="display nowrap" />

        <DataTable :options="options">
          <tr>
            <th>Date</th>
            <th>Not After</th>
            <th>Public Key Type</th>
            <th>Serial Number</th>
            <th>Subject</th>
            <th>Weak Algorithm</th>
          </tr>
          <tr>
            <td>2024-01-01</td>
            <td>2025-01-01</td>
            <td>RSA</td>
            <td>123456789</td>
            <td>CN=example.com</td>
            <td>No</td>
          </tr>
        </DataTable>
      </div>
    </div>
  </div>
</template>
