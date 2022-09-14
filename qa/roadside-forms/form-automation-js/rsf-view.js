// ==UserScript==
// @name        RSF button UI
// @namespace   Roadside forms
// @match       *://.*.jag.gov.bc.ca/roadside-forms/*
// @grant       none
// @version     1.3
// @author      -
// @description 9/9/2022, 12:00:07 PM
// ==/UserScript==

function AddButton(buttonName, topLocation, leftLocation, zIndex, fieldStructure) {
    let btn = document.createElement("button");
    btn.innerHTML = buttonName;

    buttonStyle = "top:" + topLocation + " !important;left:" + leftLocation + " !important;position:fixed;z-index: " + zIndex;
    console.log("Adding button " + buttonName + ": " + buttonStyle);
    btn.style = buttonStyle;

    btn.addEventListener('click', () => {
        FillFormSection(fieldStructure);
    })
    document.body.insertAdjacentElement("afterbegin", btn);
}

function AddLabel(labelText, topLocation, leftLocation, zIndex) {
    let lbl = document.createElement("label");
    lbl.innerHTML = labelText;

    labelStyle = "top:" + topLocation + " !important;left:" + leftLocation + " !important;position:fixed;z-index: " + zIndex;
    console.log("Adding label " + labelText + ": " + labelStyle);
    lbl.style = labelStyle;
    document.body.insertAdjacentElement("afterbegin", lbl);
}

// Labels for UI
AddLabel("Driver:", "340px", "5px", "999")
AddLabel("Vehicle:", "375px", "5px", "999")
AddLabel("Owner:", "410px", "5px", "999")
AddLabel("Disposition:", "445px", "5px", "999")
AddLabel("Prohibition:", "480px", "5px", "999")
AddLabel("Grounds:", "515px", "5px", "999")
AddLabel("Test:", "550px", "5px", "999")
AddLabel("Officer:", "585px", "5px", "999")
AddLabel("<b>Super-charged forms</b><br><br>Fill hotkeys<ul><li>Alt+1: Driver</li><li>Alt+2: Vehicle</li><li>Alt+3: Owner</li><li>Alt+4: Disposition</li><li>Alt+5: Prohibition</li><li>Alt+6: Grounds</li><li>Alt+7: Tests</li><li>Alt+8: Officer</li><li>Alt+9: Reset</li><li>Alt+0: All</li></ul>", "10px", "5px", "999")

// First test record
AddButton("1", "340px", "100px", "999", form.drivers_information);
AddButton("1", "375px", "100px", "999", form.vehicle_information);
AddButton("1", "410px", "100px", "999", form.owner);
AddButton("1", "445px", "100px", "999", form.vehicle_disposition);
AddButton("1", "480px", "100px", "999", form.prohibition);
AddButton("1", "515px", "100px", "999", form.reasonable_grounds);
AddButton("1", "550px", "100px", "999", form.test_administered);
AddButton("1", "585px", "100px", "999", form.officer);

// Second test records
AddButton("2", "340px", "130px", "999", form2.drivers_information);
AddButton("2", "375px", "130px", "999", form2.vehicle_information);
AddButton("2", "410px", "130px", "999", form2.owner);
AddButton("2", "445px", "130px", "999", form2.vehicle_disposition);
AddButton("2", "480px", "130px", "999", form2.prohibition);
AddButton("2", "515px", "130px", "999", form2.reasonable_grounds);
AddButton("2", "550px", "130px", "999", form2.test_administered);
AddButton("2", "585px", "130px", "999", form2.officer);

// Set up hotkeys to fill form sections (Alt+1 to fill driver information, etc)
document.onkeyup = function () {
    var e = e || window.event; // for IE to cover IEs window event-object
    if (e.altKey && e.which == "1".charCodeAt(0)) {
        FillFormSection(form.drivers_information);
        return false;
    } else if (e.altKey && e.which == "2".charCodeAt(0)) {
        FillFormSection(form.vehicle_information);
        return false;
    } else if (e.altKey && e.which == "3".charCodeAt(0)) {
        FillFormSection(form.owner);
        return false;
    } else if (e.altKey && e.which == "4".charCodeAt(0)) {
        FillFormSection(form.vehicle_disposition);
        return false;
    } else if (e.altKey && e.which == "5".charCodeAt(0)) {
        FillFormSection(form.prohibition);
        return false;
    } else if (e.altKey && e.which == "6".charCodeAt(0)) {
        FillFormSection(form.reasonable_grounds);
        return false;
    } else if (e.altKey && e.which == "7".charCodeAt(0)) {
        FillFormSection(form.test_administered);
        return false;
    } else if (e.altKey && e.which == "8".charCodeAt(0)) {
        FillFormSection(form.officer);
        return false;
    } else if (e.altKey && e.which == "0".charCodeAt(0)) {
        FillAllFieldsInOneGo();
        return false;
    } else if (e.altKey && e.which == "9".charCodeAt(0)) {
        ResetAllFieldsInOneGo();
        return false;
    }
}

/* --------------------------------------------------------------------
*  After page load, update layout to make room for test control buttons
*  -------------------------------------------------------------------- */

// Select the entire DOM for observing:
const target = document.querySelector('body');

// Create a new observer instance to update the app container when it appears
const observer = new MutationObserver(function () {
    // Trigger when the 'app' element loads
    if (document.getElementById('app')) {
        document.getElementById('app').style.paddingLeft = "140px"
    }
});

// Set configuration object:
const config = {childList: true};

// Start the observer
observer.observe(target, config);