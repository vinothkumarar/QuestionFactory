Progress Tracking

Purpose

Maintain current execution state.

Example

{
"project":"P1",
"chapter":"CH1",
"subtopic":"ST4",
"set":"S1",
"batch":"B1",
"question_start":1,
"question_end":10,
"status":"ACTIVE"
}

Rules

* Update after successful batch release.
* Preserve completed nodes.
* Never overwrite stable history.
* Resume generation from latest state.
