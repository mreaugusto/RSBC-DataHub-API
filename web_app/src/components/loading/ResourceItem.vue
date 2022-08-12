<template>
  <div class="row small alert text-dark py-0 my-0" v-if="! isLoaded">
    <div class="col-1 my-0">
      <b-spinner v-if=" ! isLoaded" small></b-spinner>
    </div>
    <div class="col-11 text-left">{{ resource }}</div>
  </div>

</template>

<script>
export default {
  name: "ResourceItem",
  props: {
    isLoaded: {
      type: Boolean,
      default: false
    },
    resource: {
      type: String
    }
  }
}
</script>

<style scoped>

</style>