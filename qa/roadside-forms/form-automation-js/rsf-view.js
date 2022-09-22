// ==UserScript==
// @name        RSF button UI
// @namespace   Roadside forms
// @match       *://.*.jag.gov.bc.ca/roadside-forms/*
// @grant       none
// @version     1.3
// @author      -
// @description 9/9/2022, 12:00:07 PM
// ==/UserScript==

// How far to move the page content over to make room for the hotkey menu and buttons
let sidebarWidth = "150px";

// Element id to use for the automation menu and buttons div
let automationId = "qa-automation";

// Pixel row to start the UI (how far down the page the menu starts, in pixels)
let menuStartRow = 10;
let currentRow = 1;


function AddButton(buttonName, topLocation, leftLocation, zIndex, fieldStructure) {
    let btn = document.createElement("button");
    btn.innerHTML = buttonName;

    buttonStyle = "top:" + topLocation + " !important;left:" + leftLocation + " !important;position:fixed;z-index: " + zIndex;
    console.log("Adding button " + buttonName + ": " + buttonStyle);
    btn.style = buttonStyle;

    btn.addEventListener('click', () => {
        FillFormSection(fieldStructure);
    })
    //document.body.insertAdjacentElement("afterbegin", btn);
    document.getElementById("qa-automation").appendChild(btn);
}

function AddLabel(labelText, topLocation, leftLocation, zIndex) {
    let lbl = document.createElement("label");
    lbl.innerHTML = labelText;

    labelStyle = "top:" + topLocation + " !important;left:" + leftLocation + " !important;position:fixed;z-index: " + zIndex;
    console.log("Adding label " + labelText + ": " + labelStyle);
    lbl.style = labelStyle;
    //document.body.insertAdjacentElement("afterbegin", lbl);
    document.getElementById("qa-automation").appendChild(lbl);
}

function ToggleShowHideMenu() {
    qae = document.getElementById("qa-automation");
    if (qae.style.display === "none" ) {
        qae.style.display = "block";
        document.getElementById('app').style.paddingLeft = sidebarWidth
    } else {
        qae.style.display = "none";
        document.getElementById('app').style.paddingLeft = "0px"
    }
}

function AddHotKeys() {
// Set up hotkeys to fill form sections (Alt+1 to fill driver information, etc)
    document.onkeyup = function () {
        var e = e || window.event; // for IE to cover IEs window event-object
        if (e.altKey && e.which === "H".charCodeAt(0)) {
            ToggleShowHideMenu()
            return false;
        } else if (e.altKey && e.which === "1".charCodeAt(0)) {
            FillFormSection(qaModel[0].drivers_information);
            return false;
        } else if (e.altKey && e.which === "2".charCodeAt(0)) {
            FillFormSection(qaModel[0].vehicle_information);
            return false;
        } else if (e.altKey && e.which === "3".charCodeAt(0)) {
            FillFormSection(qaModel[0].owner);
            return false;
        } else if (e.altKey && e.which === "4".charCodeAt(0)) {
            FillFormSection(qaModel[0].vehicle_disposition);
            return false;
        } else if (e.altKey && e.which === "5".charCodeAt(0)) {
            FillFormSection(qaModel[0].prohibition);
            return false;
        } else if (e.altKey && e.which === "6".charCodeAt(0)) {
            FillFormSection(qaModel[0].reasonable_grounds);
            return false;
        } else if (e.altKey && e.which === "7".charCodeAt(0)) {
            FillFormSection(qaModel[0].test_administered);
            return false;
        } else if (e.altKey && e.which === "8".charCodeAt(0)) {
            FillFormSection(qaModel[0].officer);
            return false;
        } else if (e.altKey && e.which === "0".charCodeAt(0)) {
            FillAllFieldsInOneGo();
            return false;
        } else if (e.altKey && e.which === "9".charCodeAt(0)) {
            ResetAllFieldsInOneGo();
            return false;
        }
    }
}

function AddLabelLine(labelText) {

    AddLabel(labelText, (menuStartRow + 5 + (20 * currentRow)) + "px", "20px", "999");
    currentRow++;
}

/* --------------------------------------------------------------------
*  After page load, update layout to make room for test control buttons
*  -------------------------------------------------------------------- */

// Select the entire DOM for observing:
const target = document.querySelector('body');

// Create a new observer instance to update the app container when it appears
const observer = new MutationObserver(function ()
{
    // Trigger when the 'app' element loads. Will be called multiple times
    if (document.getElementById('app'))
    {
        // Move page content over
        document.getElementById('app').style.paddingLeft = sidebarWidth

        // Add new UI div if it doesn't already exist
        if (!document.getElementById(automationId))
        {
            // Create a div to put all the UI in
            let testDiv = document.createElement("div");
            testDiv.id = automationId;
            document.body.insertAdjacentElement("afterbegin", testDiv);

            // UI Labels
            AddLabel("<b><u>Super-charged forms</u></b>", menuStartRow + "px", "5px", "999");

            AddLabelLine("<li>Alt+1: Driver</li>");
            AddLabelLine("<li>Alt+2: Vehicle</li>");
            AddLabelLine("<li>Alt+3: Owner</li>");
            AddLabelLine("<li>Alt+4: Disposition</li>");
            AddLabelLine("<li>Alt+5: Prohibition</li>");
            AddLabelLine("<li>Alt+6: Grounds</li>");
            AddLabelLine("<li>Alt+7: Tests</li>");
            AddLabelLine("<li>Alt+8: Officer</li>");
            AddLabelLine("<li>Alt+9: Reset</li>");
            AddLabelLine("<li>Alt+0: All</li>");
            AddLabelLine("<li>Alt+H: Show/hide</li>");

            AddLabel("<b><u>Fill form sections</u></b>", "310px", "5px", "999");

            AddLabel("Driver:", "340px", "5px", "999")
            AddLabel("Vehicle:", "375px", "5px", "999")
            AddLabel("Owner:", "410px", "5px", "999")
            AddLabel("Disposition:", "445px", "5px", "999")
            AddLabel("Prohibition:", "480px", "5px", "999")
            AddLabel("Grounds:", "515px", "5px", "999")
            AddLabel("Test:", "550px", "5px", "999")
            AddLabel("Officer:", "585px", "5px", "999")

            // First test record
            AddButton("1", "340px", "100px", "999", qaModel[0].drivers_information);
            AddButton("1", "375px", "100px", "999", qaModel[0].vehicle_information);
            AddButton("1", "410px", "100px", "999", qaModel[0].owner);
            AddButton("1", "445px", "100px", "999", qaModel[0].vehicle_disposition);
            AddButton("1", "480px", "100px", "999", qaModel[0].prohibition);
            AddButton("1", "515px", "100px", "999", qaModel[0].reasonable_grounds);
            AddButton("1", "550px", "100px", "999", qaModel[0].test_administered);
            AddButton("1", "585px", "100px", "999", qaModel[0].officer);

            // Second test records
            AddButton("2", "340px", "130px", "999", qaModel[1].drivers_information);
            AddButton("2", "375px", "130px", "999", qaModel[1].vehicle_information);
            AddButton("2", "410px", "130px", "999", qaModel[1].owner);
            AddButton("2", "445px", "130px", "999", qaModel[1].vehicle_disposition);
            AddButton("2", "480px", "130px", "999", qaModel[1].prohibition);
            AddButton("2", "515px", "130px", "999", qaModel[1].reasonable_grounds);
            AddButton("2", "550px", "130px", "999", qaModel[1].test_administered);
            AddButton("2", "585px", "130px", "999", qaModel[1].officer);
        }
    }
});

// Set configuration object:
const config = {childList: true};

// Start the observer
observer.observe(target, config);


AddHotKeys();