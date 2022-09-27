// ==UserScript==
// @name        RSF form data
// @namespace   Violentmonkey Scripts
// @match       *://.*.jag.gov.bc.ca/roadside-forms/*
// @grant       none
// @version     1.3
// @author      -
// @description 9/9/2022, 12:00:07 PM
// ==/UserScript==

// This is an array of JSON form scenarios. See form-record-01.js, form-record-02.js, and so on. When those files load,
// they add themselves to this array.
var qaModel = [];
