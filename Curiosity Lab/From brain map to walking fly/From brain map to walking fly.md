# From brain map to walking fly

## Research question

What has to be supplied between a connectivity map and a six-legged body simulation?

Reviews the steps between a fly nervous-system map, a neural activity model, and a walking body simulation. The conversation revises the proposed architecture to distinguish brain, descending pathways, ventral nerve cord, and motor control.

## Data and comparison design

The design keeps the anatomical chain explicit: brain, descending neurons, ventral nerve cord, motor neurons, and body actuators. Distinguish a dataset spanning brain and nerve cord from a brain-only graph, then separately specify neural dynamics and the interface to the body simulator.

## Recorded findings

| Architectural layer | Input and output | What still has to be modeled |
| --- | --- | --- |
| Brain connectome | Graph-defined neural state and descending signals | Activity dynamics are not given by a wiring diagram alone. |
| Brain-to-VNC interface | Descending signal enters a ventral nerve cord module | A direct brain-to-leg shortcut omits this intermediate circuitry. |
| VNC / motor output | Generate joint or muscle control signals | Controller dynamics and biological constraints need explicit choices. |
| Embodied simulation | Move the fly body and return sensory feedback | A closed control loop, not just a graph visualization. |

Yes. That is a real structural problem in the earlier protocol, and step 4 should be rewritten.

### The corrected architecture

A fly-walking stack has three anatomical layers:

```text
brain → descending neurons → ventral nerve cord → leg motor neurons → muscles/body
```

FlyWire primarily gives you the brain. It can support a brain-to-“walking command” experiment, but it cannot, by itself, provide the complete biological route to six legs.

BANC is the more appropriate starting dataset for a claim like:

> “The mapped nervous system drives walking.”

Because brain and ventral nerve cord are reconstructed in one volume, BANC can in principle preserve the descending-neuron-to-VNC circuitry that FlyWire omits. But BANC does not automatically provide:

- validated neural dynamics;
- complete muscle and neuromuscular-junction mapping;
- calibrated synaptic strengths;
- a ready-made mapping into FlyGym actuators;
- proof that the reconstructed circuit generates natural walking.

So the revised progression should be:

1. FlyGym body and controller.
2. BANC connectivity and cell identities.
3. A small BANC brain–VNC circuit.
4. Motor-neuron or VNC-output stimulation.
5. Neural output connected to leg actuators.
6. Only then, whole-network experiments.

FlyWire remains useful for brain-only questions and for comparing brain annotations, but it should not be presented as the complete walking substrate.

### The bistability problem

The reported runaway activity is a serious pre-integration checkpoint.

If a reproduction of the Shiu-style whole-brain model produces a small stimulus followed by persistent, nearly global activity, then you do not yet have a usable walking controller. You have a dynamical-system failure mode that must be characterized first.

The important distinction is:

- The anatomical network is published science.
- The runaway behavior is a result of a particular computational implementation and parameterization.
- It is not evidence that a living fly has seizures, nor necessarily evidence that the published model itself is biologically correct.

Likely causes include excessive recurrent gain, inappropriate treatment of excitatory/inhibitory transmitter signs, missing homeostatic mechanisms, timestep problems, or a mismatch between the repository and the paper’s intended parameters. You should not “fix” it silently by damping the network.

Before connecting anything to a body, run this test matrix:

```text
no stimulus
small pulse
larger pulse
different timestep
different random seed
zeroed recurrent input
reduced synaptic gain
```

Record:

- fraction of neurons active over time;
- mean firing rate;
- maximum firing rate;
- whether activity returns to baseline;
- whether the result changes qualitatively with timestep or gain.

A model that never returns from a tiny pulse fails the “stable neural substrate” checkpoint, regardless of how impressive its raster plot looks.

### FlyGym version concerns

The general warning about FlyGym 2.x compatibility is credible: a major-version change can alter environment constructors, action formats, actuator names, observation dictionaries, rendering, and controller interfaces.

The specific claim that “1.2.1 had known bugs” needs to be tied to a concrete GitHub issue, release note, or commit before treating it as established fact. I would not repeat that claim as settled evidence based only on reports.

More importantly, the previous recommendation to install `flygym==2.1.0` was too confident. Use the exact tag or commit associated with the example you are reproducing:

```powershell
git clone https://github.com/NeLy-EPFL/flygym
Set-Location flygym
git tag --list
git log --oneline --all --decorate -20
```

Then record:

```powershell
git rev-parse HEAD
python --version
python -m pip freeze
```

Do not mix a current FlyGym checkout with an old tutorial, old NeuroMechFly assets, or a controller written against the 1.x API.

### How to tell what actually drives the legs

The decisive question is not whether a repository contains neural code. It is:

> What value reaches the MuJoCo actuator control input immediately before each physics step?

Search the repository for the actuator boundary:

```powershell
rg -n "data\.ctrl|ctrl\[|actuator|joint_torque|torque|apply_action|env\.step|mj_step" .
```

Then trace backward from that line.

### Evidence for direct neural control

You should be able to follow a chain resembling:

```text
sensory input
→ simulated neurons
→ synapses/spikes/rates
→ motor neurons or VNC output
→ muscle/leg force
→ MuJoCo actuator
```

Look for code involving terms such as:

```powershell
rg -n "connectome|synapse|neuron|spike|motor.?neuron|descending|VNC|ventral|muscle|proprio" .
```

A strong result would show a named neural population producing a numerical motor signal that is converted into muscle forces or joint torques.

### Evidence for a controller underneath

These patterns usually indicate that walking is being generated by an engineered controller:

```powershell
rg -n "CPG|central pattern|oscillator|phase|gait|footfall|歩|rule.?based|policy|rollout|action" .
```

Especially inspect:

- `env.step(action)`;
- arrays named `action`, `torques`, `joint_targets`, or `motor_commands`;
- sinusoidal oscillators;
- phase variables;
- predefined tripod or tetrapod gait tables;
- reinforcement-learning policy outputs;
- inverse-kinematics functions;
- actuator XML files with direct joint controls.

If the leg controller receives `action` from a policy or oscillator and the neural model is only logged, visualized, or used to select a high-level mode, the walking is not being generated directly by the connectome.

### The ablation test that settles it

Run the same walking demo with the neural path disabled.

For example:

1. Replace the neural output with zeros.
2. Replace it with constant values.
3. Replace it with shuffled noise.
4. Keep the body controller and all other settings unchanged.

Interpretation:

- Walking continues normally: the controller is doing the walking.
- Walking changes only in speed or direction: the neural system is probably modulating a lower-level controller.
- Walking stops or becomes unstable: the neural output is part of the actuator path.
- The program crashes: neural activity may be required for bookkeeping, but that still does not prove it drives the legs.

Also perform the reverse test: hold the neural output fixed while disabling the CPG, policy, or rule-based controller. If walking disappears, that lower-level controller was essential.

The cleanest evidence is a signal trace showing:

```text
neural output → motor command → actuator ctrl → joint motion
```

alongside an ablation showing that removing the neural output removes the corresponding movement.

### Revised evidence labels

For this project, I would label the claims this way:

- **Published structural science:** FlyWire or BANC neuron reconstructions and synaptic connectivity.
- **Published computational science:** the specified neuron-and-synapse model, with its exact assumptions.
- **Implementation behavior:** bistability, runaway firing, numerical instability, or bugs observed in a particular repository/version.
- **Engineering integration:** converting neural activity into forces, torques, CPG commands, or FlyGym actions.
- **Biological walking claim:** established only if the BANC-derived pathway itself produces the motor commands and survives ablation/control tests.

The final architectural choice is: use BANC for the biologically complete connectome-to-walking branch, and treat FlyWire-to-FlyGym demonstrations as partial or hybrid integrations unless the code explicitly includes and uses a VNC pathway.

A connectome supplies connectivity, but it does not supply every neural dynamic, muscle parameter or control law. The final revision explicitly inserts the ventral nerve cord between brain signals and motor output. An inspectable implementation would document descending-neuron channels, VNC dynamics, motor-neuron or joint mappings, the body model and sensory feedback. Walking then becomes a test of the entire closed-loop model rather than a claim that loading the brain graph automatically generates movement.

## What the comparison shows

A reconstructed connection is not a calibrated dynamic synapse, and a simulated actuator mapping is not proof of natural walking.

## Assumptions and limits

A wiring map alone does not supply validated dynamics or a complete muscle interface. The record separates published components and proposed links rather than demonstrating a fully validated walking digital organism.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
