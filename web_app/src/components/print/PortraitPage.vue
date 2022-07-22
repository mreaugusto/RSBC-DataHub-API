<template>
  <div v-if="formData" class="svg-wrapper">
    <div id="mark-as-printed-reminder" class="alert alert-warning">
      Don't forget to return to the previous tab and mark this document as printed
    </div>
    <svg width="100%" :viewBox="viewbox">
      <image :href="baseURL + page.image.filename" :height="page.image.height + 'px'" :width="page.image.width + 'px'"/>
      <component
        v-for="(field, index) in fieldsToShow"
        v-bind:key="index"
        :is="fields[field].field_type + 'Component'"
        :start="fields[field].start"
        :field="fields[field]"
        :form_type="form_type"
        :form_id="form_id"
        :field_name="field"
        :form_data="formData">
      </component>
     Sorry, your browser does not support inline SVG.
    </svg>
  </div>
</template>

<script>

import PageCommon from "@/components/print/PageCommon";

export default {
  name: "PortraitPage",
  mixins: [PageCommon]
}
</script>

<style scoped>

   .svg-wrapper {
     border-bottom: darkblue solid 1px;
   }

  @media print {
     #roadsafety-header {
       display: none;
     }
     #debug-component {
       display: none;
     }
     #not-authenticated-banner {
       display: none;
     }

     #mark-as-printed-reminder {
       display: none;
     }

    .svg-wrapper {
      margin-top: 25mm;
      border: none;
      page-break-before:always;
    }

    @page {
      margin: 0;

    }
  }

</style>