<template>
  <b-modal id="new-user" :hide-header="true" :hide-footer="true">
    <label for="search">
      Lookup a new user by their BCeID username
      <div class="small text-muted">(You can't lookup users at other agencies)</div>
    </label>
    <multiselect v-model="selectedUsers" id="search" label="last_name" track-by="code"
                 placeholder="Search for a new user by username" open-direction="bottom"
                 :options="users" :multiple="true" :searchable="true"
                 :loading="isLoading" :internal-search="false"
                 :clear-on-select="false" :close-on-select="false"
                 :options-limit="300" :limit="3" :limit-text="limitText"
                 :max-height="600" :show-no-results="false" :hide-selected="true"
                 @search-change="userLookupApi" @remove="clearAll" @select="userSelect">
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
    <div class="card mt-4" v-if="userFound">
      <div class="card-body bg-light">


        <validation-observer v-slot="{handleSubmit, validate}">
          <form @submit.prevent="handleSubmit(onSubmit(validate))">
            <admin-text-field id="first_name" :errors="errors" :value="new_user.first_name" @update="adminUpdate">First Name</admin-text-field>
            <admin-text-field id="last_name" :errors="errors" :value="new_user.last_name" @update="adminUpdate">Last Name</admin-text-field>
            <admin-text-field id="badge_number" :errors="errors" :value="new_user.badge_number" @update="adminUpdate">Badge Number</admin-text-field>
            <admin-text-field id="agency" :errors="errors" :value="new_user.agency" @update="adminUpdate">Agency</admin-text-field>
            <admin-role-field id="roles" :errors="errors" :value="new_user.roles" @update="adminUpdate">Roles</admin-role-field>

            <div @click="showGuid = ! showGuid" class="text-right">
              <b-icon-dot variant="info"></b-icon-dot>
            </div>
            <div class="text-muted small" v-if="showGuid">
              <div>Business GUID: {{ new_user.business_guid }}</div>
              <div>User GUID: {{ new_user.user_guid }}</div>
            </div>


            <div class="row">
              <div class="col-12 text-right">
                <b-button size="sm" variant="light" @click="cancelModal" class="btn-outline-primary">
                  Close without creating
                </b-button>
                <b-button @click="onSubmit(validate)" size="sm" variant="primary" class="ml-3">
                  Create user
                </b-button>
              </div>
            </div>
          </form>
        </validation-observer>
      </div>
    </div>

  </b-modal>
</template>

<script>

import {mapActions, mapGetters} from "vuex";
import Vue from 'vue'
import AdminTextField from "@/components/admin/AdminTextField";
import AdminRoleField from "@/components/admin/AdminRoleField";
import { ValidationObserver } from 'vee-validate';
import Multiselect from 'vue-multiselect'

export default {
  name: "NewUserModal",
  components: {AdminTextField, ValidationObserver, AdminRoleField, Multiselect},
  data() {
    return {
      new_user: {},
      errors: {},
      selectedUsers: [],
      users: [],
      isLoading: false,
      userFound: false,
      showGuid: false
    }
  },
  computed: {
    ...mapGetters(["getCurrentUserObject"]),
  },
  methods: {
    ...mapActions(["createUser", "bceidUserLookup"]),
    limitText (count) {
      return `and ${count} other users`
    },
    cancelModal() {
      this.$bvModal.hide('new-user')
    },
    userLookupApi(username) {
      this.isLoading = true
      this.bceidUserLookup(username).then(response => {
        this.users = response
        this.isLoading = false
      })
      .catch( () => {
        this.isLoading = false
      })
    },
    clearAll() {
      this.selectedUsers = []
      this.userFound = false
      this.new_user = {}
    },
    userSelect(userObject) {
      console.log("userSelect()", userObject)
      this.new_user = userObject
      this.isLoading = false
      this.userFound = true
    },
    onSubmit() {
      this.createUser([this.getCurrentUserObject, this.new_user])
        .then( () => {
          console.log("localCreateUser - success")
          this.clearAll()
          this.errors = {}
          this.$bvModal.hide('new-user')
        })
        .catch( (errors) => {
          console.log("localCreateUser - fail", errors)
          this.errors = errors
        })
    },
    adminUpdate(event) {
      Vue.set(this.new_user, event[0], event[1])
    }
  },
}
</script>
