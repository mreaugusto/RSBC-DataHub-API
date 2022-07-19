<template>
  <div class="form-group">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors }">
      <label v-if="show_label" :for="id"><slot></slot></label>
      <input :type="input_type"
             :disabled="disableInput"
             class="form-control"
             :class="errors.length > 0 ? 'border-danger bg-warning' : ''"
             :id="id"
             :placeholder="placeholder"
             v-model="attribute">
      <div class="small text-danger">{{ getError }}</div>
    </validation-provider>
  </div>
</template>

<script>
export default {
  name: "AdminTextField",
  props: {
    errors: null,
    disabled: {
      type: Boolean,
      default: false
    },
    placeholder: null,
    input_type: {
      type: String,
      default: 'text'
    },
    id: null,
    show_label: {
      type: Boolean,
      default: true
    },
    value: null
  },
  data() {
    return {
      rules: null
    }
  },
  computed: {
    getError() {
      if(this.errors && this.id in this.errors) {
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
  }
}
</script>

<style scoped>

</style>