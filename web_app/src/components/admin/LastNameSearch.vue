<template>
  <div>
    <multiselect v-model="selectedUsers" id="search" label="last_name" track-by="code"
                 placeholder="Filter authorized users by last name" open-direction="bottom"
                 :options="users" :multiple="true" :searchable="true"
                 :loading="isLoading" :internal-search="false"
                 :clear-on-select="false" :close-on-select="false"
                 :options-limit="300" :limit="3" :limit-text="limitText"
                 :max-height="600" :show-no-results="false" :hide-selected="true"
                 @search-change="asyncFind" @remove="clearAll" @select="asyncSelect">
      <template slot="tag" slot-scope="{ option, remove }">
        <span class="custom__tag">
          <span>{{ option.last_name }}</span>
          <span class="custom__remove" @click="remove(option)">❌</span>
        </span>
      </template>
      <template slot="clear" slot-scope="props">
        <div class="multiselect__clear" v-if="selectedUsers.length" @mousedown.prevent.stop="clearAll(props.search)"></div>
      </template>
      <span slot="noResult">No user by that last name</span>
    </multiselect>
  </div>
  
</template>

<script>

import Multiselect from 'vue-multiselect'
import {mapActions, mapGetters, mapMutations} from "vuex";

export default {
  name: "LastNameSearch",
  
  components: {
    Multiselect
  },
  data () {
    return {
      selectedUsers: [],
      users: [],
      isLoading: false
    }
  },
  computed: {
    ...mapGetters(["getCurrentUserObject"]),
  },
  methods: {
    ...mapActions(["adminFetchAllUsers"]),
    ...mapMutations(["updateAdminUsers"]),
    limitText (count) {
      return `and ${count} other users`
    },
    asyncFind (last_name) {
      this.isLoading = true
      this.adminFetchAllUsers([this.getCurrentUserObject, last_name]).then(response => {
        this.users = response
        this.isLoading = false
        if (this.selectedUsers.length > 0) {
          this.updateAdminUsers(this.selectedUsers)
        }
      })
    },
    asyncSelect (user) {
      this.asyncFind(user.last_name)
    },
    clearAll () {
      this.isLoading = true
      this.selectedUsers = []
      this.adminFetchAllUsers([this.getCurrentUserObject, '']).then(response => {
        this.isLoading = false
        this.updateAdminUsers(response)
      })
    }
  }
}
</script>

<style scoped>

</style>