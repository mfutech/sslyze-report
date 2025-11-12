<script setup>
import * as bootstrap from 'bootstrap';
import jszip from 'jszip';
import DataTable from 'datatables.net-vue3'
import DataTablesCore from 'datatables.net-bs5';
import 'datatables.net-buttons-bs5';
import 'datatables.net-buttons/js/buttons.html5.mjs';

// @import url('bootstrap');
// @import url('datatables.net-bs5');
// @import url('datatables.net-buttons-bs5');

DataTablesCore.use(bootstrap);
DataTablesCore.Buttons.jszip(jszip);
DataTable.use(DataTablesCore);

const columns = [
    { data: 'date', title: 'Date' },
    { data: 'not_after', title: 'Not After' },
    { data: 'public_key_type', title: 'Public Key Type' },
    { data: 'serial_number', title: 'Serial Number' },
    { data: 'subject', title: 'Subject' },
    { data: 'weak_algo', title: 'Weak Algorithm' },

];

const data = [
    {
        date: "maaintenant",
        not_after: 'today',
        public_key_type: "pubkey",
        serial_number: '000',
        subject: 'un truc',
        weak_algo: 'no weak'

    },
    {
        date: "maaintenant",
        not_after: 'today',
        public_key_type: "pubkey",
        serial_number: '000',
        subject: 'un truc',
        weak_algo: 'no weak'

    }, {
        date: "maaintenant",
        not_after: 'today',
        public_key_type: "pubkey",
        serial_number: '000',
        subject: 'un truc',

        weak_algo: 'no weak'

    }
];

const options = {
    responsive: true,
    select: true,
    layout: {
        topStart: {
            buttons: ['copy', 'csv', 'excel', 'pdf', 'print']
        }
    }
};
</script>

<template>

    <div>
        <div class="row">
            <div class="col-xl-2"> </div>
            <div class="col-xl-8">
                test
                <DataTable :columns="columns" :options="options" :data="data" class="display nowrap" />
            </div>
            <div class="col-xl-2"> </div>
        </div>
    </div>
</template>