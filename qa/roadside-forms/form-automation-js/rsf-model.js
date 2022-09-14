// ==UserScript==
// @name        RSF form data
// @namespace   Violentmonkey Scripts
// @match       *://.*.jag.gov.bc.ca/roadside-forms/*
// @grant       none
// @version     1.3
// @author      -
// @description 9/9/2022, 12:00:07 PM
// ==/UserScript==

// Values for form fields, named after element id
var form2 = {
    drivers_information: {
        drivers_number:  "1234567",
        drivers_licence_jurisdiction: "ALBERTA",
        last_name:       "Catgurgles",
        first_name:      "Katie",
        dob:             "19990909",
        address1:        "77 Seventh St South",
        driver_phone:    "111-000-2222",
        city:            "Boston Bar",
        postal:          "V1V 2V2",
        province:        "Alberta"
    },
    vehicle_information: {
        plate_number:   "AA057A",
        plate_province:  "ALBERTA",
        plate_year: "2022",
        plate_val_tag: "02",
        registration_number: "REG-12345",
        vehicle_type: "random",
        vehicle_year: "random",
        vehicle_make: "random",
        vehicle_color: "random",
        vin_number: "VIN012345679",
        puj_code: "ALBERTA",
        nsc_number: "NSC1234567890"
    },
    owner: {
        owners_last_name: "Bathbottom",
        owners_first_name: "Barry B.",
        owners_address1: "1, One Way West",
        owners_city: "CALGARY",
        owners_province: "ALBERTA",
        owners_postal: "A1A 1A1",
        owners_phone: "403-000-6789"
    },
    vehicle_disposition: {
//    "vehicle_impounded_no,No": true,
        "vehicle_impounded_yes,Yes": true,
        "location_of_keys_driver,With driver": true,  // 12-hour form
        "location_of_keys_WITH DRIVER,With driver": true, // 24-hour form
//    "location_of_keys_WITH VEHICLE,With vehicle": true, // 24-hour form
//    "location_of_keys_vehicle,With vehicle": true,       // 24-hour form
//    "ilo_multiselect": "AGGRESSIVE AUTO TOWING LTD, 34523 2ND AVE, ABBOTSFORD, 604-854-5669"
        ilo_multiselect: "random",
        vehicle_released_to: "Phillip McFootpayne",
        released_date: "**today**",
        released_time: "**now**",
//    "ilo_multiselect": "AGGRESSIVE AUTO TOWING LTD, 34523 2ND AVE, ABBOTSFORD, 604-854-5669"
        ilo_multiselect: "random"
    },
    prohibition: {
        //"prohibition_type_12hr_alcohol,Alcohol 90.3(2)": true,   // 12-hour
        "prohibition_type_12hr_drugs,Drugs 90.3(2.1)": true,   // 12-hour
        //"prohibition_type_alcohol,Alcohol 215(2)": true,       // 24-hour
        "prohibition_type_drugs,Drugs 215(3)": true,           // 24-hour
        offence_address: "CAT ST / RAT ROAD",
        offence_city: "random",
        file_number: "RSI-1234",
        prohibition_start_date: "**today**",
        prohibition_start_time: "**now**"
    },
    reasonable_grounds: {
        officer: true,
        admission: false,
        witness: true,
        video: false,
        other: true,
        operating_ground_other: "Reasonable grounds reason number 22.",
        "prescribed_device_yes,Yes": true,
        //"prescribed_device_no,No": true,
        "reason_prescribed_test_not_used_refused,Refused by driver": true,
        //"reason_prescribed_test_not_used_opinion,Opinion formed the driver was affected by alcohol and/or drugs": true,
        test_date: "**today**",
        test_time: "**now**"
    },
    test_administered: {  // Only appears on 24-hour form

        // Alcohol: Alco-Sensor FST (ASD)
        //"test_administered_asd,Alco-Sensor FST (ASD)": true,  //Alcohol, when selected fill out ASD expiry and result
        //asd_expiry_date: "**today**",
        //"result_alcohol_under,51-99 mg%": true,  // Alcohol
        //"result_alcohol_over,Over 99 mg%": true,  // Alcohol

        // Alcohol:  Approved Instrument
        //"test_administered_instrument,Approved Instrument": true,  // Alcohol, when selected fill out BAC Result
        //test_result_bac: 789,

        // Alcohol and drugs: Prescribed Physical Coordination Test (SFST)
        "test_administered_sfst,Prescribed Physical Coordination Test (SFST)": true,

        // Drugs: Approved Drug Screening Equipment
        //"test_administered_adse,Approved Drug Screening Equipment": true,  // Drugs, when selected fill test result
        //thc: true,  // Drug checkbox
        //cocaine: true,  // Drug checkbox

        // Drugs: Prescribed Physical Coordination Test (DRE)
        //"test_administered_dre,Prescribed Physical Coordination Test (DRE)": true, // Drugs
    },
    officer: {
        agency: "BOSTON BAR RCMP",
        badge_number: "RSI-911",
        officer_name: "LUNGPAYNE"
    }
};

var form = {
    drivers_information: {
        drivers_number:  "1234567",
        drivers_licence_jurisdiction: "British Columbia",
        last_name:       "Dogsneeze",
        first_name:      "Davey",
        dob:             "20000101",
        address1:        "88 Eigth Avenue East",
        driver_phone:    "250-000-1111",
        city:            "Ashcroft",
        postal:          "V2V 9V9",
        province:        "British Columbia"
    },
    vehicle_information: {
        plate_number:   "888 HHH",
        plate_province:  "BRitish columbia",
        plate_year: "2022",
        plate_val_tag: "02",
        registration_number: "REG-12345",
        vehicle_type: "random",
        vehicle_year: "random",
        vehicle_make: "random",
        vehicle_color: "random",
        vin_number: "VIN012345679",
        puj_code: "BRITISH COLUMBIA",
        nsc_number: "NSC0000000009"
    },
    owner: {
        owners_last_name: "Tottenham",
        owners_first_name: "Terry T.",
        owners_address1: "99 Ninth Lane North",
        owners_city: "PRINCETON",
        owners_province: "BRITISH COLUMBIA",
        owners_postal: "V3V 3V3",
        owners_phone: "250-111-9999"
    },
    vehicle_disposition: {
    "vehicle_impounded_no,No": true,
//        "vehicle_impounded_yes,Yes": true,
        "location_of_keys_driver,With driver": true,  // 12-hour form
//    "location_of_keys_vehicle,With vehicle": true,
        "location_of_keys_WITH VEHICLE,With vehicle": true, // 24-hour form
//        "location_of_keys_WITH DRIVER,With driver": true, // 24-hour form
        "reason_for_not_impounding_released,Released to other driver": true,
        //"reason_for_not_impounding_roadside,Left at roadside": true,
        vehicle_released_to: "Peter P. Potterthwaite",
        released_date: "**today**",
        released_time: "**now**",
//    "ilo_multiselect": "AGGRESSIVE AUTO TOWING LTD, 34523 2ND AVE, ABBOTSFORD, 604-854-5669"
        ilo_multiselect: "random"
    },
    prohibition: {
        "prohibition_type_12hr_alcohol,Alcohol 90.3(2)": true,   // 12-hour
        //"prohibition_type_12hr_drugs,Drugs 90.3(2.1)": true,   // 12-hour
        "prohibition_type_alcohol,Alcohol 215(2)": true,       // 24-hour
        //"prohibition_type_drugs,Drugs 215(3)": true,           // 24-hour

        offence_address: "ELEPHANT WALK @ LAMA LANE",
        offence_city: "random",
        file_number: "RSI-1234",
        prohibition_start_date: "**today**",
        prohibition_start_time: "**now**"
    },
    reasonable_grounds: {
        officer: false,
        admission: true,
        witness: false,
        video: true,
        other: false,
        operating_ground_other: "Reasonable grounds reason number 22.",
        "prescribed_device_yes,Yes": true,
        //"prescribed_device_no,No": true,
        //"reason_prescribed_test_not_used_refused,Refused by driver": true,
        "reason_prescribed_test_not_used_opinion,Opinion formed the driver was affected by alcohol and/or drugs": true,
        test_date: "**today**",
        test_time: "**now**"
    },
    test_administered: {  // Only appears on 24-hour form

        // Alcohol: Alco-Sensor FST (ASD)
        "test_administered_asd,Alco-Sensor FST (ASD)": true,  // Alcohol, when selected fill out ASD expiry and result
        asd_expiry_date: "20300330",
        "result_alcohol_under,51-99 mg%": true,  // Alcohol
        //"result_alcohol_over,Over 99 mg%": true,  // Alcohol

        // Alcohol:  Approved Instrument
        //"test_administered_instrument,Approved Instrument": true,  // Alcohol, when selected fill out BAC Result
        //test_result_bac: 789,

        // Alcohol and drugs: Prescribed Physical Coordination Test (SFST)
        //"test_administered_sfst,Prescribed Physical Coordination Test (SFST)": true,

        // Drugs: Approved Drug Screening Equipment
        //"test_administered_adse,Approved Drug Screening Equipment": true,  // Drugs, when selected fill test result
        //thc: true,  // Drug checkbox
        //cocaine: true,  // Drug checkbox

        // Drugs: Prescribed Physical Coordination Test (DRE)
        //"test_administered_dre,Prescribed Physical Coordination Test (DRE)": true, // Drugs
    },
    officer: {
        agency: "PRINCETON RCMP",
        badge_number: "RSI-999",
        officer_name: "TRACEY"
    }
};

