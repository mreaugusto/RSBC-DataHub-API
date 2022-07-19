<template>
    <b-modal :id="modal_id" size="lg"
             :no-close-on-esc="true"
             :no-close-on-backdrop="true"
             :hide-header="true" :hide-footer="true">
      <div>Are you sure you want to delete <span class="font-weight-bold">{{ user.last_name }}, {{ user.first_name }}</span>?</div>
      <div class="row">
        <div class="col-12 text-right">
          <b-button size="sm" variant="secondary" @click="cancelModal">
            Cancel
          </b-button>
          <b-button @click="onDelete" size="sm" variant="danger" class="ml-3">
            Delete user
          </b-button>
        </div>
      </div>
      <template #modal-footer="{ ok, cancel }">
        <b-button size="sm" variant="danger" @click="onDelete">
          Delete User
        </b-button>
        <b-button size="sm" variant="success" @click="cancel()">
          Cancel
        </b-button>
      </template>
    </b-modal>

</template>

<script>

import {mapActions, mapGetters} from "vuex";

export default {
  name: "DeleteUserModal",
  props: {
    modal_id: null,
    user: {
      first_name: '',
      last_name: '',
      badge_number: '',
      user_guid: '',
      username: {},
      roles: []
    }
  },
  computed: {
    ...mapGetters(["getCurrentUserObject"])
  },
  methods: {
    ...mapActions(["adminDeleteUser"]),
    cancelModal() {
      this.$bvModal.hide(this.modal_id)
    },
    onDelete() {
      this.adminDeleteUser([this.getCurrentUserObject, this.user.user_guid])
        .then( () => {
          console.log("onDelete() - success")
          this.$bvModal.hide(this.modal_id)
        })
        .catch( (errors) => {
          console.log("onDelete() - fail", errors)
          this.errors = errors
        })
    }
  }
}
</script>

<style scoped>

</style>