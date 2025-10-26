<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Host Details</h1>
        <hr><br><br>
        <router-link :to="{ name: 'home' }" type="button" class="btn btn-success btn-sm">Back to home</router-link>
        <br><br>
        <h1>{{ host }}:{{ port }}</h1>

        <table class="table table-hover">
          <tbody>
            <tr>
              <th>Last Scan Date</th>
              <td colspan="2">{{ last_scan.date }}</td>
            </tr>
            <tr>
              <th>SSLv2 Enabled</th>
              <td>{{ last_scan.sslv2.enabled ? 'Yes' : 'No' }}</td>
              <td>{{ last_scan.sslv2.accepted_ciphers }}</td>
            </tr>
            <tr>
              <th>SSLv3 Enabled</th>
              <td>{{ last_scan.sslv3.enabled ? 'Yes' : 'No' }}</td>
              <td>{{ last_scan.sslv3.accepted_ciphers }}</td>

            </tr>
            <tr>
              <th>TLS 1.0 Enabled</th>
              <td>{{ last_scan.tls1_0.enabled ? 'Yes' : 'No' }}</td>
              <td>{{ last_scan.tls1_0.accepted_ciphers }}</td>

            </tr>
            <tr>
              <th>TLS 1.1 Enabled</th>
              <td>{{ last_scan.tls1_1.enabled ? 'Yes' : 'No' }}</td>
              <td>{{ last_scan.tls1_1.accepted_ciphers }}</td>

            </tr>
            <tr>
              <th>TLS 1.2 Enabled</th>
              <td>{{ last_scan.tls1_2.enabled ? 'Yes' : 'No' }}</td>
              <td>{{ last_scan.tls1_2.accepted_ciphers }}</td>

            </tr>
            <tr>
              <th>TLS 1.3 Enabled</th>
              <td>{{ last_scan.tls1_3.enabled ? 'Yes' : 'No' }}</td>
              <td>{{ last_scan.tls1_3.accepted_ciphers }}</td>

            </tr>
            <tr>
              <th>Mozilla Old Compliant</th>
              <td>{{ last_scan.moz_old.compliant ? 'Yes' : 'No' }}</td>
              <td>{{ last_scan.moz_old.feedback }} <br />
                <ul v-for="issue in moz_old_issues" :key="issue.name">
                  <li><strong>{{ issue.name }}:</strong> {{ issue.description }}</li>
                </ul>
              </td>
            </tr>
            <tr>
              <th>Mozilla Intermediate Compliant</th>
              <td>{{ last_scan.moz_intermediate.compliant ? 'Yes' : 'No' }}</td>
              <td>{{ last_scan.moz_intermediate.feedback }} <br />
                <ul v-for="issue in moz_intermediate_issues" :key="issue.name">
                  <li><strong>{{ issue.name }}:</strong> {{ issue.description }}</li>
                </ul>
              </td>
            </tr>
            <tr>
              <th>Mozilla Modern Compliant</th>
              <td>{{ last_scan.moz_modern.compliant ? 'Yes' : 'No' }}</td>
              <td>{{ last_scan.moz_modern.feedback }} <br />
                <ul v-for="issue in moz_modern_issues" :key="issue.name">
                  <li><strong>{{ issue.name }}:</strong> {{ issue.description }}</li>
                </ul>
              </td>
            </tr>
            <!-- <tr>
              <th>Certificate Serial Numbers</th>
              <td>
                <div v-for="serial in last_scan.certificate_serial_number" :key="serial">
                  <router-link :to="{ name: 'certificate', params: { serial: serial } }" class="btn btn-primary btn-sm">
                    {{ serial.length > 18 ? serial.substr(0, 15) + '...' : serial }}
                  </router-link>
                </div>
              </td>
            </tr> -->
          </tbody>
        </table>

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
      last_scan: null,
      scans: [],
      columns: [
        { title: 'Date', data: 'date' },
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
    fetchHostDetails() {
      const path = '/api/host/' + this.host + '/' + this.port;
      axios.get(path)
        .then((response) => {
          if (response.data.status === 'success') {
            this.scans = response.data.scans;
            this.last_scan = this.scans[0];
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
  computed: {
    moz_intermediate_issues() {
      if (this.last_scan) {
        if (this.last_scan.moz_intermediate) {
          return Object.entries(this.last_scan.moz_intermediate.issues)
            .map(([key, val]) => {
              return { name: key, description: val };
            })
        }
      }
      return [];
    },
    moz_old_issues() {
      if (this.last_scan) {
        if (this.last_scan.moz_old) {
          return Object.entries(this.last_scan.moz_old.issues)
            .map(([key, val]) => {
              return { name: key, description: val };
            })
        }
      }
      return [];
    },
    moz_modern_issues() {
      if (this.last_scan) {
        if (this.last_scan.moz_modern) {
          return Object.entries(this.last_scan.moz_modern.issues)
            .map(([key, val]) => {
              return { name: key, description: val };
            })
        }
      }
      return [];
    },
  },
};
</script>
