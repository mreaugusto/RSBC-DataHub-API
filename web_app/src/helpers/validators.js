import moment from 'moment';
import {extend} from "vee-validate";

extend('secret', {
  validate: value => value === 'example',
  message: 'This is not the magic word'
});

extend('required', {
  validate(value) {
    return {
      required: true,
      valid: ['', null, undefined].indexOf(value) === -1
    };
  },
  message: "This field is required",
  computesRequired: true
});

extend('validDt', {
  validate: value => moment(value, "YYYYMMDD", true).isValid(),
  message: "That's not a valid date"
});

// extend('validDtTime', {
//   validate(value) {
//     console.log("validDtTime " + value)
//     return {
//       required: true,
//       valid: moment(value, "YYYYMMDD HHmm", true).isValid()
//     };
//   },
//   message: "That's not a valid date time"
// });

extend('notExpired', {
  validate: value => moment().diff(moment(value, 'YYYYMMDD', true), 'days') < 0,
  message: "Expired"
});

extend('notFutureDt', {
  validate(value) {
    return {
      required: true,
      valid: moment().diff(moment(value), 'minutes') > 0,
    };
  },
  message: "Cannot be future dated",
  computesRequired: true
});

// digits 8
extend('dob8', {
  validate(value) {
    let result = false;
    const regexMatch = value.match("^[0-9]{4}[0-9]{2}[0-9]{2}$")
    if (Array.isArray(regexMatch)) {
       result = regexMatch[0] === value;
    }
    return {
      valid: result
    };
  },
  message: "DOB must have 8 digits",
});

extend('dob', {
  validate(value) {
    return {
      required: true,
      valid: moment().diff(moment(value), 'years') > 0,
    };
  },
  message: "DOB cannot be future dated",
  computesRequired: true
});


extend('phone', {
  validate(value) {
    let result = false;
    const regexMatch = value.match("^[0-9]{10}$")
    if (Array.isArray(regexMatch)) {
       result = regexMatch[0] === value;
    }
    return {
      valid: result
    };
  },
  message: "Phone number format ##########"
});


extend('lt25', {
  validate(value) {
    return {
      valid: value.length <= 25,
    };
  },
  message: "too long; must be less 25 chars",
});


extend('lt5', {
  validate(value) {
    return {
      valid: value.length <= 5,
    };
  },
  message: "Value must be less than 5 chars",
});

extend('lt3', {
  validate(value) {
    return {
      valid: value.length < 3,
    };
  },
  message: "Value must be less than 3 chars",
});

extend('lt4', {
  validate(value) {
    return {
      valid: value.length < 5,
    };
  },
  message: "Value must be than 5 chars",
});


