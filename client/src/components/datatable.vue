<script setup lang="ts">
import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net';
import 'datatables.net-responsive';
import 'datatables.net-select';

DataTable.use(DataTablesCore);

const columns = [
    { data: 'date', title: 'Date' },
    { data: 'not_after', title: 'Not After' },
    { data: 'public_key_type', title: 'Public Key Type' },
    { data: 'serial_number', title: 'Serial Number' },
    { data: 'subject', title: 'Subject' },
    { data: 'weak_algo', title: 'Weak Algorithm' },

];

const options = {
    responsive: true,
    select: true,
};
</script>

<template>
    <DataTable :columns="columns" :options="options" ajax="http://localhost/api/certificates" class="display nowrap" />
</template>