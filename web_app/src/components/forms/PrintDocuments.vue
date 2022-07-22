<template>
  <div id="print-row" class="row">
    <button :disabled="isDocumentServed(path)" @click="onSubmit(validate)" class="btn btn-primary mr-3" id="btn_print_forms">
      Validate and prepare documents
      <b-spinner v-if="display_spinner" small label="Loading..."></b-spinner>
    </button>
    <div class="small text-danger pt-2">
      <fade-text v-if="isNotValid" :key="rerender" show-seconds=3000>Errors in form - check for validation errors above</fade-text>
    </div>
    <router-link v-if="isDocumentServed(path) && show_certificate" :to="{ name: 'cos', params: { id: form_object.form_id, form_type: form_object.form_type}}" target="_blank">
      <div class="btn btn-primary">Print Certificate of Service</div>
    </router-link>
    <!-- Modal Start -->
    <b-modal id="is-served" title="Did you print and serve the driver?" size="lg"
             @ok="onSuccessfulServe"
             :no-close-on-esc="true"
             :no-close-on-backdrop="true"
             :hide-header="true">

      <div class="card mb-2">
        <div class="card-body">
          <div class="row">
            <div class="col-8">
              The documents are ready for printing.  Once the documents have been
              printed and delivered to the driver, return to this page to mark the
              documents as {{ servedWording.toLowerCase() }}.
            </div>
            <div class="col-4 text-right">
              <router-link :to="{ name: 'print', params: { id: form_object.form_id, form_type: form_object.form_type}}" target="_blank">
                <div class="btn btn-primary">Create Documents</div>
              </router-link>
              <p class="small text-muted">Opens in a new tab</p>
            </div>
          </div>
        </div>
      </div>

      <div class="card" v-if="show_certificate">
        <div class="card-body">
          <service-certificate-wording
            :served_date="getServedDateString"
            :form_full_name="getOfficialFormName(path)"
            :certified_date="getCertifiedDateString"
            :form_id="formattedNoticeNumber(path)"
            :driver_name="concatenateDriverName(path)"
            :officer_name="getAttributeValue(path, 'officer_name')"
            :badge_number="getAttributeValue(path, 'badge_number')"
            :agency="getAttributeValue(path, 'agency')">
          </service-certificate-wording>
        </div>
      </div>

      <template #modal-footer="{ ok, cancel }">
        <b-button size="sm" variant="success" @click="ok()">
          {{ servedWording }}
        </b-button>
        <b-button size="sm" variant="danger" @click="cancel()">
          Not {{ servedWording }}
        </b-button>
      </template>
    </b-modal>
    <!-- Modal End -->
  </div>
</template>

<script>
import moment from "moment-timezone";
import ServiceCertificateWording from "@/components/print/ServiceCertificateWording";
import fadeText from "../FadeText";
import {mapActions, mapGetters, mapMutations} from "vuex";
import constants from "@/config/constants";

export default {
  name: "PrintDocuments",
  props: {
    show_certificate: {
      type: Boolean,
      default: false
    },
    path: {
      type: String,
      default: ''
    },
    form_object: {
      type: Object
    },
    validate: {},
    variants: {
      type: Array
    }
  },
  data() {
    return {
      display_spinner: false,
      isNotValid: false,
      rerender: 1
    }
  },
  computed: {
    ...mapGetters([
        "getOfficialFormName",
        "formattedNoticeNumber",
        "concatenateDriverName",
        "isDocumentServed",
        "getAttributeValue",
        "getCurrentlyEditedForm",
        "getCurrentlyEditedFormData",
        "getCurrentlyEditedFormObject",
    ]),
    getCertifiedDateString() {
      return moment().tz(constants.TIMEZONE).format("YYYY-MM-DD")
    },

    getServedDateString() {
      return moment().tz(constants.TIMEZONE).format("Do MMMM, YYYY")
    },
    servedWording() {
      if (this.show_certificate) {
        return "Served"
      } else {
        return "Printed"
      }
    }
  },
  methods: {
    ...mapActions(["tellApiFormIsPrinted", "saveCurrentFormToDB"]),
    ...mapMutations(["setFormAsPrinted"]),
    onSuccessfulServe() {
      const current_timestamp = moment().tz(constants.TIMEZONE).format()
      let payload = {}
      payload['form_object'] = this.form_object
      payload['variants'] = this.variants;
      payload['form_data'] = this.form_object.data;
      payload['timestamp'] = current_timestamp
      console.log("onSuccessfulServe()", payload)
      this.setFormAsPrinted(payload)
      this.saveCurrentFormToDB(this.form_object)
      this.tellApiFormIsPrinted(this.form_object)
        .then( (response) => {
            console.log("response from tellApiFormIsPrinted()", response)
        })
        .catch( (error) => {
            console.log("no response from tellApiFormIsPrinted()", error)
        })
    },

    async onSubmit (validate) {
      this.display_spinner = true;
      const is_validated = await validate()
      console.log('inside onSubmit()', is_validated);
      if(is_validated) {
        this.$bvModal.show("is-served")
        this.display_spinner = false;

      } else {
        this.rerender++;
        this.isNotValid = true;
      }
      this.display_spinner = false;
    }
  },
  components: {
    fadeText,
    ServiceCertificateWording
  }
}
</script>

<style scoped>

  #print-row {

    margin: 0 0 0 0;
    padding: 0 0 0 0;
  }

</style>
