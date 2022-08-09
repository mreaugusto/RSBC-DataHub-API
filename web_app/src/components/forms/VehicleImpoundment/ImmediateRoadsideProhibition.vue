<template>
  <form-card title="Immediate Roadside Prohibition">
    <form-row>
      <radio-field id="irp" :path="path"
                   fg_class="col-sm-6" :options='[["yes", "Yes"], ["no", "No"]]'
                   rules="required">3, 7  or 30 Day Impoundment <span class="text-muted">In accordance
                    with Section 215.46 and 253 of the Motor Vehicle Act</span>
      </radio-field>
    </form-row>
    <div v-if="getAttributeValue(path, 'irp_yes')">
      <form-row >
        <radio-field id="duration" :path="path + '/irp_yes'"
                     fg_class="col-sm-6" :options='[["3-day", "3-Day"], ["7-day", "7-Day"], ["30-day", "30-Day"]]'
                     rules="required">Duration
        </radio-field>
      </form-row>
      <form-row>
        <text-field id="ipr_number" :path="path + '/irp_yes'" fg_class="col-sm-6">IRP Number</text-field>
      </form-row>
    </div>

  </form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "ImmediateRoadsideProhibition",
  mixins: [CardsCommon]
}

</script>

<style scoped>

</style>