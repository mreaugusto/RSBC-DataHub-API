<template>
  <div v-if="isUserAnAdmin && getCurrentUserObject['business_guid']">
    <div class="row">
      <div class="col-4 text-left input-group">
        <last-name-search></last-name-search>
      </div>
      <div class="col-8 text-right">
        <b-button v-b-modal.new-user class="btn btn-primary small">
          <b-icon icon="plus"></b-icon>Add user
        </b-button>
      </div>
    </div>

    <div class="card w-100 mt-3 mb-3" >
      <div class="card-header text-white text-left font-weight-bold small pl-3 pt-1 pb-1 bg-primary">
        Authorized Users
      </div>
      <div class="card-body text-left pb-1">
        <table class="table table-striped">
          <tbody>
            <tr>
              <th>First</th>
              <th>Last</th>
              <th>Badge</th>
              <th>Agency</th>
              <th>User GUID</th>
              <th>Roles</th>
              <th colspan="2">Action</th>
            </tr>
            <admin-user-row v-for="(user, index) in this.getAllUsers" :key="index" :user="user"></admin-user-row>

          </tbody>
        </table>
      </div>
    </div>
    <new-user-modal></new-user-modal>
  </div>
</template>

<script>

import {mapActions, mapGetters, mapMutations} from "vuex";
import AdminUserRow from "@/components/admin/AdminUserRow";
import NewUserModal from "@/components/admin/NewUserModal";
import LastNameSearch from "@/components/admin/LastNameSearch";

export default {
  name: "Admin",
  data() {
    return {
      search: ''
    }
  },
  computed: {
    ...mapGetters(['isUserAnAdmin','getCurrentUserObject', "getAllUsers"]),
  },
  methods: {
    ...mapActions(['adminFetchAllUsers', 'fetchStaticLookupTables']),
    ...mapMutations(["updateAdminUsers"])
  },
  mounted() {
    this.fetchStaticLookupTables( {"resource": "users", "admin": false, "static": false})
      .then(currentUser => {
        return currentUser
      })
      .then( (currentUser) => {
        console.log("currentUser:", currentUser)
        this.adminFetchAllUsers([currentUser, '']).then(data => {
          this.updateAdminUsers(data)
        })
      })

  },
  components: {
    LastNameSearch,
    AdminUserRow, NewUserModal
  }
}
</script>

<style scoped>

</style>