# Digital Forms quality assurance (testing)

This is a collection of projects for manual and automated testing in the Digital Forms project:

- **apr**: Application for prohibition review. This project uses Orbeon Forms and a Python back-end to give prohibited drivers to request their prohibition to be reviewed by RSBC. Set up in fall 2020. Developed by Jonathan Longe. Uses a VIPS API (see 'ntt-dfapi' folder below). 
- **icbc-vi-irp-apir**: This is an ICBC API to which 12-hour suspension notices and 24-hour prohibition notices are sent after the forms are printed by a police officer using the roadside forms project (see 'roadside-forms' folder below).
- **ntt-dfapi**: This is a VIPS API used by the application for prohibition review (APR) project. This allows applications for prohibition review (see 'apr' project above) to send and retrieve information from VIPS. Developed by NTT (Shaun Millar, Kyle Flood) in fall of 2020.
- **ntt-irp-api**: This API allows information from roadside forms to be sent directly into VIPS. Developed in summer of 2022 by NTT (Shaun Millar).
- **roadside-forms**: These digital road-side forms are filled out by police and issued to offending drivers. The project uses Python and Vue.js (Vuex) where each form is a single-page app.
- **script**: helper scripts.


## Further documentation

For more test documentation, see the Digital Forms testing [Confluence wiki page](https://justice.gov.bc.ca/wiki/display/RDFP/Digital+Forms+project+testing). 