<template>
  <div class="form-group">
    <validation-provider :rules="rules" :name="id">
      <label :for="id">Roles</label>
      <multiselect v-model="attribute"
                   :id="id"
                   tag-placeholder="That's not an option"
                   placeholder="Select user's roles"
                   :multiple="true"
                   :taggable="true"
                   :options="['officer', 'administrator', 'agency_admin']"></multiselect>
      <div class="small text-danger">{{ getError }}</div>
    </validation-provider>
  </div>
</template>

<script>

import Multiselect from "vue-multiselect";


export default {
  name: "AdminRoleField",
  props: {
    rules: null,
    errors: {},
    id: null,
    value: null
  },
  data() {
    return {

    }
  },
  computed: {
    getError() {
      if(this.id in this.errors) {
        return this.errors[this.id][0]
      }
      return ''
    },
    attribute: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit("update", [this.id, value])
      }
    },
    disableInput() {
      return this.disabled ? 'disabled' : null
    }
  },
  components: {Multiselect}
}
</script>

<style scoped>

</style>