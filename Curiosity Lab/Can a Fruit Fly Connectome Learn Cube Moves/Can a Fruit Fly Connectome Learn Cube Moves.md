# Can a Fruit Fly Connectome Learn Cube Moves

**Creator:** @MinLiBuilds  

## Research question

Can a fixed connectivity pattern route learned task information directly to selected motor-neuron outputs?

Investigates whether a fixed fruit-fly connectome topology can be trained by changing its weights so that cube-move decisions are expressed through identified leg motor neurons, rather than decoded first and translated into leg actions afterward. The archived workflow includes frozen-reservoir comparisons, constrained motor-neuron readouts, and an EfficientCube teacher-distillation workflow using rank-8 LoRA and states at scramble depths 1–9.

## Data and comparison design

Distinguish three conditions: a frozen reservoir, a restricted motor-neuron readout, and trained weights constrained by the original topology. Keep teacher-action mapping and LoRA training separate from later multistep closed-loop evaluation.

## Recorded findings

| Workflow stage | Recorded work | What must be separated |
| --- | --- | --- |
| Graph-inspired model | Connectome-based architecture and cube-state inputs | A design inspired by connectivity, not a biological cube-solving experiment. |
| Supervised training | Learn actions from teacher examples | Teacher labels define the behavior being transferred. |
| Action convention | Teacher action mapping was corrected | A wrong move convention can invalidate apparently trained behavior. |
| Closed-loop evaluation | Apply successive predicted moves to cube states | Distinct from single-step agreement; no removed success rates are restored. |

The archive documents the training and teacher-distillation workflow, including correction of the teacher’s action mapping. The introduction retains that method without adding an unverified cube-solving success rate.

The model conditions answer progressively different questions. A frozen reservoir asks whether fixed graph-constrained dynamics provide a useful representation to a trained readout. Restricting the readout to motor-neuron outputs tests whether that interface retains useful information. Allowing weights to train while retaining the topology tests a broader learned system, rather than the unmodified biological connectome.

1. Encode a cube state and the allowed action vocabulary consistently across the learner and teacher.
2. Compare fixed internal dynamics with restricted readouts and topology-constrained training.
3. Inspect the teacher-to-model move mapping before trusting a distilled checkpoint.
4. Evaluate sequences of predicted moves on updated cube states, separately from single-step imitation.

The archive’s action-mapping correction is consequential: a learner can fit labels under the wrong convention while failing when its output is interpreted as a physical cube move. The corrected workflow is therefore an inspectable training study. It is not evidence that a fruit fly’s actual nervous system understands a puzzle.

## What the comparison shows

An action-classification target is not a whole-animal behavior claim. Physical movement and closed-loop solving would require separate validation.

## Sources and research materials

Creator attribution follows the signature on the supplied poster and matches Case Index.csv. The original session export and poster are preserved from AIPOCH-Creator-Use-Cases.zip. This introduction describes the archived research workflow.
