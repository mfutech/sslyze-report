<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <MenuHeader :title="'Host Details: ' + host + ':' + port" />

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

        <HostsList :hosts="scans" />
        <!-- <DataTable :data="scans" :columns="columns" class="table table-hover display nowrap" /> -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';
import HostsList from '../components/HostsList.vue';
import MenuHeader from '../components/MenuHeader.vue';

export default {
  components: { HostsList, MenuHeader },
  data() {
    return {
      host: this.$route.params.host,
      port: this.$route.params.port,
      last_scan: null,
      scans: [],
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
