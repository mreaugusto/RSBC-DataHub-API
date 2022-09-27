// ==UserScript==
// @name        RSF form filler
// @namespace   Roadside forms
// @match       *://.*.jag.gov.bc.ca/roadside-forms/*
// @grant       none
// @version     1.3
// @author      -
// @description 9/9/2022, 12:00:07 PM
// ==/UserScript==

// Set a Vue.js Radio button
async function SetRadioButton(field_id)
{
    console.debug(` - Selecting radio button ${field_id}`);
    document.getElementById(field_id).click();
}

// Set a Vue.js Checkbox
async function SetCheckbox(field_id, value)
{
    console.debug(` - Selecting checkbox ${field_id}`);

    checkbox = document.getElementsByName(field_id);
    if (checkbox !== null)
    {
        // Checkbox should be checked
        if (value === true) {
            if (!checkbox[0].checked)
                checkbox[0].click()
        }
        else if (value === false) {
            if (checkbox[0].checked)
                checkbox[0].click()
        }
    }
}

// Set a Vue.js text field value
async function SetField(field_id, value)
{
    console.debug(` - Filling text field "${field_id}": "${value}"`);
    el = document.getElementById(field_id);
    if (value === "**today**")
    {
        let today = new Date();
        let day = String (today.getDate()).padStart(2, '0');
        let month = String (today.getMonth()+1).padStart(2, '0');
        let year = today.getFullYear();
        el.value = `${year}${month}${day}`;
    }
    else if (value === "**now**")
    {
        let today = new Date();
        let hours = today.getHours();

        // Subtract five minutes so as not to trigger the form's time validation
        let minutes = today.getMinutes() - 5;
        if (minutes < 0)
        {
            minutes = 60+minutes;
            hours--;
        }
        hourString = String (hours).padStart(2, '0')
        minuteString = String (minutes).padStart(2, '0')
        el.value = `${hourString}${minuteString}`;
    }
    else if (value === "**phone**")
    {
        el.value = chance.phone().replace("(", "").replace(") ", "-")
    }
    else if (value === "**address**")
    {
        el.value = chance.address();
    }
    else if (value === "**birthdate**")
    {
        el.value = dateToYMD(chance.birthday({type: "adult"}));
    }
    else if (value === "**postal**")
    {
        el.value = chance.postal();
    }
    else if (value === "**email**")
    {
        el.value = chance.email();
    }
    else
    {
        el.value  = value;
    }
    await el.dispatchEvent(new Event('input'));
}

function dateToYMD(date) {
    var d = date.getDate();
    var m = date.getMonth() + 1; //Month from 0 to 11
    var y = date.getFullYear();
    return '' + y + (m<=9 ? '0' + m : m) + (d <= 9 ? '0' + d : d);
}

// Set a Vue.js multiselect/drop-down value
async function SetMultiselect(field_id, value)
{
    console.debug(` - Filling multiselect ${field_id}: ${value}`);
    el = document.getElementById(field_id);

    // Don't bother setting the value if it's already set
    if (el.parentElement.getElementsByClassName('multiselect__single').length)
    {
        var currentValue = el.parentElement.getElementsByClassName('multiselect__single')[0].innerText;
        if (currentValue === value.toUpperCase())
        {
            console.debug(`   ${field_id} is already set to ${currentValue}`);
            return;
        }
    }

    await el.dispatchEvent(new Event ('focus'));
    pickableElements = el.parentElement.parentElement.parentElement.getElementsByClassName('multiselect__element');

    if (value === "random")
    {
        randomItem = Math.floor(Math.random() * pickableElements.length);
        // For vehicle colour(s) field having maximum of two colours selected returns no available options
        if (pickableElements.length > 0)
        {
            pickableElements[randomItem].getElementsByClassName('multiselect__option')[0].click();
        }
        return;
    }
    else
    {
        // Iterate through multiselect options looking for the desired value...
        for (const i in pickableElements)
        {
            if (pickableElements[i].innerText === value.toUpperCase())
            {
                pickableElements[i].getElementsByClassName('multiselect__option')[0].click();
                return;
            }
        }
    }
    console.error(`Could not find element on form: ${field_id}`);
}

// Fill out all the fields in a section of the form
async function FillFormSection(fieldStructure) {
    console.debug("Filling form section " + JSON.stringify(fieldStructure))

    // Iterate fields, filling values from JSON
    for (var fieldId in fieldStructure) {
        formElement = document.getElementById(fieldId);

        // Checkbox elements have duplicate ids, so find with name instead of id
        if (formElement == null) {
            if (document.getElementsByName(fieldId).length > 0) {
                await SetCheckbox(fieldId, fieldStructure[fieldId]);
            } else {
                console.debug(` - Element ${fieldId} does not exist on the form. Skipping...`);
            }
            continue;
        }

        // Text fields, multiselects, radio buttons, and unknown
        if (formElement.className.startsWith('form-control')) {
            await SetField(fieldId, fieldStructure[fieldId]);
        } else if (formElement.className.startsWith('multiselect__input')) {
            await SetMultiselect(fieldId, fieldStructure[fieldId]);
        } else if (formElement.className.startsWith('form-check-input')) {
            await SetRadioButton(fieldId, fieldStructure[fieldId]);
        } else {
            console.error(`Unknown form element: ${fieldId}`);
        }
    }
}

async function ClearFormSection(fieldStructure) {
    console.debug(`Clearing form section ${fieldStructure.toString()}:`)
    // Iterate fields, filling values from JSON
    for (var fieldId in fieldStructure) {
        if (document.getElementById(fieldId).className.startsWith('form-control')) {
            await SetField(fieldId, "");
        } else if (document.getElementById(fieldId).className.startsWith('multiselect__input')) {
            if (fieldId === "province" || fieldId === "plate_province") {
                await SetMultiselect(fieldId, "BRITISH COLUMBIA");
            } else {
                await SetMultiselect(fieldId, "");
            }
        } else if (document.getElementById(fieldId).className.startsWith('form-check-input')) {
            if (document.getElementById(fieldId).type === "radio") {
                await SetRadioButton(fieldId, "");
            } else if (document.getElementById(fieldId).type === "checkbox") {
                await SetCheckbox(fieldId, "");
            } else {
                console.error(`Unknown element type for ${fieldId}.`)
            }
        } else {
            console.error(`Unknown form element: ${fieldId}`);
        }
    }
}

async function FillAllFieldsInOneGo() {
    await FillFormSection(qaModel[0]["drivers_information"]);
    await FillFormSection(qaModel[0]["vehicle_information"]);
    await FillFormSection(qaModel[0]["owner"]);
    await FillFormSection(qaModel[0]["vehicle_disposition"]);
    await FillFormSection(qaModel[0]["prohibition"]);
    await FillFormSection(qaModel[0]["reasonable_grounds"]);
    await FillFormSection(qaModel[0]["test_administered"]);
    await FillFormSection(qaModel[0]["officer"]);
}

async function ResetAllFieldsInOneGo() {
    await ClearFormSection(qaModel[0]["drivers_information"]);
    await ClearFormSection(qaModel[0]["vehicle_information"]);
    await ClearFormSection(qaModel[0]["owner"]);
    await ClearFormSection(qaModel[0]["vehicle_disposition"]);
    await ClearFormSection(qaModel[0]["prohibition"]);
    await ClearFormSection(qaModel[0]["reasonable_grounds"]);
    await ClearFormSection(qaModel[0]["test_administered"]);
    await ClearFormSection(qaModel[0]["officer"]);
}