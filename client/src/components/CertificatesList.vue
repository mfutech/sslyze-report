<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Certificates_list</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Book</button>
        <a href="/Ping" type="button" class="btn btn-primary btn-sm">Ping</a>
        <br><br>
        <DataTable class="table table-hover">
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
        </DataTable>

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
        </hr>
        <DataTable ajax="/api/certificates" class="display">
        </DataTable>
        <hr>
        data table with data prop
        <DataTable :options="options" :data="others" class="display nowrap" />
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
  name: 'CertificatesList',
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
