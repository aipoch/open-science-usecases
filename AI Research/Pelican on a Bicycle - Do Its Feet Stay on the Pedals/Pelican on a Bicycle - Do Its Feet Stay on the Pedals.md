# Pelican on a Bicycle: Do Its Feet Stay on the Pedals?

A convincing cycling animation needs more than spinning wheels. The rider's feet must follow the pedals, the knees must bend without changing limb length, and wheel rotation must agree with the bicycle's travel. This case follows an AI coding session that built a procedural Three.js scene and checked those relationships in saved numeric evidence and browser captures.

The archived scene places a stylised pelican on a cruiser bicycle travelling around a coastal road. The central question is deliberately narrower than whether the scene looks attractive: **does the animation preserve contact and synchronization as speed, camera view and playback state change?**

## The question

It is easy to animate a bicycle and a rider as separate objects. It is harder to keep them connected through a complete pedal stroke. A foot can drift away from its pedal, a knee can stretch, or a wheel can appear to slide along the road even when each individual motion looks plausible.

The user requested a working interactive application, with procedural models, a continuously cycling rider, adjustable speed, pause and resume, camera orbit, zoom and multiple views. The archive contains the implementation, test records, screenshots, launch instructions and verification report. It is one implementation case; it does not compare multiple models or establish a general coding benchmark score.

## What was built

| Component | Archived implementation | Why it matters |
|---|---|---|
| Scene | Procedural pelican, bicycle and coastal environment | The main objects are generated in code rather than replaced with an image or prerecorded animation. |
| Bicycle | Wheels, crank, pedals, 44-tooth chainring and 18-tooth rear cog | The drivetrain gives wheel rotation and pedal cadence a shared numerical relationship. |
| Rider | Two-bone inverse kinematics for legs and wings | The knees and elbows adapt to moving contact targets while limb lengths remain fixed. |
| Motion | Rear contact-point travel along a closed road | Travel distance drives rotation, placement, steering and lean. |
| Interaction | Speed slider, pause/resume, four views, orbit, zoom, skeleton overlay and reset | These controls expose whether the animation remains coherent when playback and viewpoint change. |

The project vendors Three.js r160 and includes JavaScript, HTML and CSS. The supplied README describes a roughly 796 m closed route, a 0.34 m wheel radius and a 0–36 km/h speed range. The pelican is stylised: its wings act as arms, and it continues to balance upright when stopped.

## How the motion stays connected

The simulation uses the rear tyre contact point's distance along the lane as its main state. For each frame, distance increases by `speed × elapsed time`. Rear-wheel rotation then increases by `distance / wheel radius`. The front wheel uses the travel of its own contact point.

The crank follows the wheel through the fixed gear ratio: `wheel turns per crank turn = 44 / 18`, approximately **2.44444**. This prevents the wheel, pedals and bicycle translation from running on unrelated animation clocks.

The foot targets are attached to the pedal positions. An analytic two-segment solver positions each knee between its hip and ankle, using a 0.45 m thigh and a 0.44 m shin. A corresponding shoulder–elbow–wrist solver keeps the wing tips at the handlebar grips. Path curvature sets steering and lean; secondary body motion follows the crank phase.

This construction matters when interpreting the result. A reported zero foot-to-pedal gap is a check that the implemented scene graph preserves an intended contact constraint. It is not an independent measurement of a free foot finding a pedal, nor evidence that a real pelican could ride a bicycle.

## What the archived checks show

The evidence comes from the supplied research package. The numeric records were reviewed during publication preparation; the application was not independently rerun as a new browser experiment for this introduction.

| Evidence layer | What can be checked in the archive | Recorded outcome |
|---|---|---|
| Browser UI and live scene | `browser-test.json`, captured in WebKit with WebGL 2 | All **17 listed checks** are marked passed. |
| Browser mechanical self-test | `browser-selftest.json`, four speeds over 30 simulated seconds each | Foot and wrist contact gaps are recorded as 0 m; the gear relationship and IK reachability checks pass. |
| Headless logic and geometry | `selftest.json`, Node harness without a browser or WebGL | All **36 listed checks** are marked passed. |
| Visual evidence | Archived browser screenshots and an eight-phase software contact sheet | Show the scene, controls and rider pose; stills alone do not establish continuous motion. |

**Counting correction:** the original verification report and final session message describe “18 of 18” browser checks. The saved `browser-test.json` contains 17 check objects. This introduction uses the directly countable total of 17 and preserves the original research package unchanged.

### Four speeds, one synchronization rule

The table below summarizes the saved browser mechanical self-test. Each row represents **30 simulated seconds**, rather than a separate physical trial. Slip is the cumulative discrepancy between simulated contact-point travel and wheel roll; smaller values indicate closer numerical agreement in this implementation.

| Speed (km/h) | Distance (m) | Rear slip (mm) | Front slip (mm) | Cadence (rpm) | Knee-angle range |
|---|---:|---:|---:|---:|---|
| 6 | 50 | 0.0111 | 0.00185 | 19.1 | 74.2–138.7° |
| 16.2 | 135 | 0.0642 | 0.00105 | 51.7 | 74.2–138.7° |
| 28 | 233.3333 | 0.161 | 0.00220 | 89.4 | 74.2–138.8° |
| 36 | 300 | 0.236 | 0.000991 | 114.9 | 74.2–138.8° |

Across those four records, wheel turns per crank turn remain approximately 2.444444, foot-to-pedal and wrist-to-grip gaps are recorded as 0 m, and the leg targets remain reachable. The largest saved rear slip is **0.236 mm over 300 m** at 36 km/h. These values characterize the recorded kinematic simulation and its measurement procedure, not tyre friction on a real road.

### Live controls and rendering

The browser evidence records matching travel and wheel-roll distances of 12.06 m, a 2.44444 wheel-to-crank ratio, and about **74 fps over 200 frames at a 1440 × 900 viewport** on one Apple GPU. The scene records 779,926 triangles in that browser capture. This is one hardware and rendering configuration, not a promise of the same frame rate on other devices.

The listed UI checks cover view selection, pausing while rendering continues, resuming with Space, camera orbit beyond a full turn, wheel zoom, the speed slider, skeleton visibility and reset. Input was driven by synthetic DOM events; the archive does not establish the experience of a person using a mouse or a touchscreen.

## What the comparison shows

| A visually plausible result | The stronger question asked here | Evidence available |
|---|---|---|
| A pelican appears to pedal | Do the feet remain at the pedal targets throughout tested motion? | World-space contact checks in the four-speed records |
| Wheels spin while the bicycle moves | Does rotation agree with travel distance and the 44:18 drivetrain? | Live-frame measurements and mechanical self-tests |
| A camera button changes the view | Does it reach the intended side, and can the camera still orbit while paused? | Saved browser UI checks |
| A single screenshot looks polished | Was the scene rendered in a browser, and which visual defects were corrected? | WebKit captures and the archived verification report |

The useful lesson is how to turn a visual coding request into checks on contact, geometry, synchronization and interaction. It does not establish superiority over another model, another implementation or a human developer.

## Limits and interpretation

- **Browser coverage:** the archived run used WebKit/WKWebView. Chrome and Firefox were not exercised in that run.
- **Launch coverage:** the README's normal route is an HTTP static server. The original environment blocked a listening port, so the browser evidence used file access in WebKit; the HTTP server script was syntax-checked rather than demonstrated end to end.
- **Input coverage:** synthetic pointer, wheel and keyboard events were checked. Human input and touch pinch zoom were not verified.
- **Physical realism:** both wheels follow the same lane line; the road is not banked; the rider never freewheels or puts a foot down. Straight-ahead toe clearance does not establish clearance at full steering lock.
- **Motion evidence:** the supplied package contains numeric tests and stills, not a recorded demo video. Software previews and real WebGL screenshots are different evidence types.
- **Scope:** this is an AI-built animation with kinematic constraints, not a validated biological model or a comparative model evaluation.

## Explore the archived project

The saved `pelican-bicycle.zip` contains the application source, vendored Three.js, tools, screenshots and test evidence. Its README explains how to serve the extracted project locally with Node or Python. The verification document lists the checks, visual defects fixed during development and remaining limitations.

Useful questions when continuing the project include testing the normal HTTP launch in additional browsers, checking real pointer and touch controls, measuring performance on lower-power hardware, and testing clearance at larger steering angles. Those are follow-up checks, not results already established by this archive.

The public case title was set for publication. The native session retains its original title, **Interactive 3D Pelican Riding a Bicycle with Three.js**. The published package is a byte-for-byte copy of the supplied export with a renamed outer filename; its internal research record has not been rewritten.
