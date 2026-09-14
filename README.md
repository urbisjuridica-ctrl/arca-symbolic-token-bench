---
license: mit
task_categories:
- text-generation
language:
- es
- en
tags:
- ai-benchmark
- symbolic-reasoning
- hermeneutics
- agents
size_categories:
- n<1K
configs:
  - config_name: benchmark
    data_files:
      - split: train
        path: "arca_alianza_hermeneutics_v1.json"
  - config_name: dataset_sft
    data_files:
      - split: train
        path: "arca_alianza_sft.jsonl"
---

# AGENTES-ARCA-DE-LA-ALIANZA

A high-difficulty micro-benchmark designed to challenge Large Language Models (LLMs) and Autonomous Agents on two complex fronts: **multi-layer semantic interpretation (hermeneutics)** and **strictly controlled creativity**.

## 🧠 The Challenge
Most standard evaluation sets test literal understanding or factual retrieval. **ARCA-DE-LA-ALIANZA** introduces a high-density symbolic framework where the AI agent must operate on literal, symbolic, and abstract levels simultaneously, without breaking character or succumbing to unconstrained hallucinations.

## 🧪 What it evaluates:
- **Role & Instruction Fidelity:** Rigorous adherence to a tight, non-standard interpretive framework under cognitive pressure.
- **Symbol Grounding:** Correctly assigning conceptual functions to abstract entities within the prompt context.
- **Controlled Creativity:** Forcing the LLM to generate a coherent deep reading while bound to strict theoretical constraints.

## 📦 Repository Structure
- `arca_alianza_hermeneutics_v1.json`: Evaluation item ready for automated testing pipelines.
- `arca_alianza_sft.jsonl`: Supervised Fine-Tuning (SFT) training example format.

## 📄 License & Collaboration
This project is open-source under the **MIT License**. It is fully open and free for humanity to support the democratic advancement of safe, aligned, and deeply capable AI agents. For academic work, please refer to the repository's `CITATION.cff` on GitHub.
