// Values for form fields, named after element id
qaModel.push({
    drivers_information: {
        drivers_number:  "1234567",
        drivers_licence_jurisdiction: "ALBERTA",
        last_name:       "Catgurgles",
        first_name:      "Katie",
        dob:             "**birthdate**",
        address1:        "77 Seventh St South",
        driver_phone:    "**phone**",
        city:            "Boston Bar",
        postal:          "**postal**",
        province:        "Alberta",
        driver_gender:   "Female",
        expiry_year:     "2025",
        dl_class:        "5"
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
        owners_address1: "**address**",
        owners_city: "CALGARY",
        owners_province: "ALBERTA",
        owners_postal: "**postal**",
        owners_phone: "**phone**",
        owners_email: "**email**"
    },
    vehicle_disposition: {
        impounded_dt: "**today**",
//    "vehicle_impounded_no,No": true,
        "vehicle_impounded_yes,Yes": true,
        "location_of_keys_driver,With driver": true,  // 12-hour form
        "location_of_keys_WITH DRIVER,With driver": true, // 24-hour form
//    "location_of_keys_WITH VEHICLE,With vehicle": true, // 24-hour form
//    "location_of_keys_vehicle,With vehicle": true,       // 24-hour form
        ilo_multiselect: "random",
        vehicle_released_to: "Phillip McFootpayne",
        released_date: "**today**",
        released_time: "**now**",
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
        prohibition_start_time: "**now**",
        "prohibition_type_3-days-warn,3 days WARN": false,
        "prohibition_type_7-days-warn,7 days WARN": true,
        "prohibition_type_30-days-warn,30 days WARN": false,
        "prohibition_type_90-days-fail,90 days FAIL": false,
        "prohibition_type_90-days-refuse,90 days REFUSAL": false
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
        test_time: "**now**",
        reason_excessive_speed: false,
        reason_prohibited: true,
        reason_suspended: false,
        reason_racing: true,
        reason_stunt: false,
        reason_motorcycle_seating: true,
        reason_motorcycle_restrictions: false,
        reason_unlicensed: true,
        ul_prohibition_number: "00123456",
        "suspected_bc_resident_yes,Yes": false,
        "suspected_bc_resident_no,No": true
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
});