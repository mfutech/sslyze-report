<template>
    <h1>{{ title }}</h1>
    <hr>
    <router-link :to="{ name: 'hostslist' }" type="button" class="btn btn-outline-info btn-sm">Hosts List</router-link>
    &nbsp;
    <router-link :to="{ name: 'certificateslist' }" type="button" class="btn btn-outline-info btn-sm">Certificates
        List</router-link>
    <br><br>
</template>
<script>
export default {
    props: ['title'],
}
</script>