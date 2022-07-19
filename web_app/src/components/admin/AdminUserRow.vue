<template>
  <tr>
    <td class="small">{{ user.first_name }}</td>
    <td class="small">{{ user.last_name }}</td>
    <td class="small">{{ user.badge_number }}</td>
    <td class="small">{{ user.agency }}</td>
    <td class="small text-muted">{{ user.user_guid }}</td>
    <td>
      <h2 v-for="(role, idx) in user.roles" :key="idx" class="badge badge-secondary ml-2">
          {{ role }}
      </h2>
    </td>
    <td>
      <b-button v-b-modal="editModalId" class="btn-success btn btn-sm" >
        Edit
      </b-button>
      <b-button v-b-modal="deleteModalId" class="btn-danger btn btn-sm ml-3">
        Delete
      </b-button>
    </td>
    <edit-user-modal :user="user" :modal_id="editModalId"></edit-user-modal>
    <delete-user-modal :user="user" :modal_id="deleteModalId"></delete-user-modal>
  </tr>
</template>

<script>

import { mapGetters} from "vuex";
import DeleteUserModal from "@/components/admin/DeleteUserModal";
import EditUserModal from "@/components/admin/EditUserModal";

export default {
  name: "AdminUserRow",
  data() {
    return {
      approveSpinner: false,
      deleteSpinner: false
    }
  },
  props: {
    user: {
      first_name: '',
      last_name: '',
      badge_number: '',
      user_guid: ''
    }
  },
  computed: {
    ...mapGetters(['isUserAnAdmin']),
    editModalId() {
      return 'edit-user-' + this.user.user_guid
    },
    deleteModalId() {
      return 'delete-user-' + this.user.user_guid
    }
  },
  components: {
    DeleteUserModal,
    EditUserModal
  }
}
</script>

<style scoped>

</style>