# Can a Fruit Fly Connectome Learn Cube Moves

**Creator:** @MinLiBuilds

## Research question

Can a fixed connectivity pattern route learned task information directly to selected motor-neuron outputs?

## Data and method

Distinguish three conditions: a frozen reservoir, a restricted motor-neuron readout, and trained weights constrained by the original topology. Keep teacher-action mapping and LoRA training separate from later multistep closed-loop evaluation.

## Recorded findings

Investigates whether a fixed fruit-fly connectome topology can be trained by changing its weights so that cube-move decisions are expressed through identified leg motor neurons, rather than decoded first and translated into leg actions afterward. The archived workflow includes frozen-reservoir comparisons, constrained motor-neuron readouts, and an EfficientCube teacher-distillation workflow using rank-8 LoRA and states at scramble depths 1–9.

The archive documents the training and teacher-distillation workflow, including correction of the teacher’s action mapping. The introduction retains that method without adding an unverified cube-solving success rate.

## What the findings mean

An action-classification target is not a whole-animal behavior claim. Physical movement and closed-loop solving would require separate validation.

## Scope

The study evaluates a computational model built from connectome topology. Action classification and complete multistep cube solving are separate evaluation tasks.

## Package and provenance

Creator attribution follows the signature on the supplied poster and matches Case Index.csv. The original session export and poster are preserved from AIPOCH-Creator-Use-Cases.zip. This introduction describes the archived research workflow.
