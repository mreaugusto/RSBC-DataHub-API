
export default {

    // Calculate the check digit of a six-digit prohibition number
    checkDigit(prohibition_number) {
        const n = Array.from(prohibition_number.toString()).map(Number);
        const number_sum = (
            n[0] +
            this.timesTwo(n[1]) +
            n[2] +
            this.timesTwo(n[3]) +
            n[4] +
            this.timesTwo(n[5]))
        return number_sum % 10
    },

    // If number * 2 is greater than 9, return 1
    // otherwise return the number * 2
    timesTwo(number) {
        return parseInt(((number * 2).toString()).split()[0])
    },


    getAdminRootUrl(api_root, current_user, append_string)  {
        if(current_user.roles.includes("agency_admin")) {
            return api_root + "/api/v1/agency/" + current_user.business_guid + append_string
        } else {
            return api_root + "/api/v1/admin" + append_string
        }
    }

}