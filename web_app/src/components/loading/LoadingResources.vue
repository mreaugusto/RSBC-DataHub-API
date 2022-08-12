<template>
  <div v-if=" ! allResourcesLoaded" class="card mb-3">
    <div class="card-body">
      <div class="text-dark text-left small font-weight-bold">Loading resources ...</div>
      <resource-item v-for="(status, index) in getLoadingStatus"
                     v-bind:key="index"
                     :is-loaded="status"
                     :resource="index">
      </resource-item>
    </div>
  </div>
</template>


<script>
import {mapGetters} from "vuex";
import ResourceItem from "@/components/loading/ResourceItem";


export default {
  name: "LoadingResources",
  components: {ResourceItem},
  computed: {
  ...mapGetters(["getLoadingStatus", "allResourcesLoaded", "getFirstNotLoaded"])
  }
}
</script>

<style scoped>

</style>