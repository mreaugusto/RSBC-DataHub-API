<template>
  <b-modal :id="modal_id" :hide-header="true" :hide-footer="true">
    <validation-observer v-slot="{handleSubmit, validate}">
      <form @submit.prevent="handleSubmit(onSubmit(validate))">
        <admin-text-field id="first_name" :errors="errors" :value="modified_user.first_name" @update="adminUpdate">First Name</admin-text-field>
        <admin-text-field id="last_name" :errors="errors" :value="modified_user.last_name" @update="adminUpdate">Last Name</admin-text-field>
        <admin-text-field id="badge_number" :errors="errors" :value="modified_user.badge_number" @update="adminUpdate">Badge Number</admin-text-field>
        <admin-text-field id="agency" :errors="errors" :value="modified_user.agency" @update="adminUpdate">Agency</admin-text-field>
        <admin-role-field id="roles" :errors="errors" :value="modified_user.roles" @update="adminUpdate">Roles</admin-role-field>
        <div class="row">
          <div class="col-12 text-right">
            <b-button size="sm" variant="light" @click="cancelModal" class="btn-outline-primary">
              Close without saving
            </b-button>
            <b-button @click="onSubmit(validate)" size="sm" variant="primary" class="ml-3">
              Save user
            </b-button>
          </div>
        </div>
      </form>
    </validation-observer>
  </b-modal>
</template>

<script>

import {mapActions, mapGetters} from "vuex";
import Vue from 'vue'
import AdminTextField from "@/components/admin/AdminTextField";
import { ValidationObserver } from 'vee-validate';
import AdminRoleField from "@/components/admin/AdminRoleField";

export default {
  name: "EditUserModal",
  components: {AdminRoleField, AdminTextField, ValidationObserver},
  props: {
    modal_id: null,
    user: {
      agency: '',
      first_name: '',
      last_name: '',
      badge_number: '',
      roles: []
    },
    value: null
  },
  data() {
    return {
      modified_user: {},
      errors: {}
    }
  },
  computed: {
    ...mapGetters(["getCurrentUserObject"]),
  },
  methods: {
    ...mapActions(["adminEditUser"]),
    onSubmit() {
      this.adminEditUser([this.getCurrentUserObject, this.modified_user])
        .then( () => {
          console.log("localCreateUser - success")
          this.$bvModal.hide(this.modal_id)
        })
        .catch( (errors) => {
          console.log("localEditUser - fail", errors)
          this.errors = errors
        })
    },
    adminUpdate(event) {
      Vue.set(this.modified_user, event[0], event[1])
    },
    cancelModal() {
      this.$bvModal.hide(this.modal_id)
    },
  },
  mounted() {
    this.modified_user = { ...this.user }
  }
}
</script>