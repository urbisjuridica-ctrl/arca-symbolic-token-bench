import json
import os
from datetime import datetime
from transformers import AutoTokenizer

def export_tokenomics_report():
    print("[+] Generando reporte actualizado de Tokenomics (HEKT-NOVA v2.1)...")

    tokenizer_name = "hf-internal-testing/llama-tokenizer"
    try:
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    except Exception as e:
        print(f"[!] Error al cargar el tokenizador: {e}")
        return

    dataset_path = "data/arca_symbolic_benchmark.jsonl"
    if not os.path.exists(dataset_path):
        print(f"[!] No se encontró el dataset en {dataset_path}")
        return

    compact_mapping = {
        "[HEKT-NOVA::ONTOLOGICAL_ALIGNMENT]": "[H::ALN]",
        "[HEKT-NOVA::PQC_LATTICE]": "[H::PQC]",
        "[HEKT-NOVA::SMART_CONTRACT]": "[H::SMC]",
        "[HEKT-NOVA::VRAM_MANAGEMENT]": "[H::VRM]",
        "RECURSIVE_ALIGN": "REC",
        "SHOR_RESISTANT": "SHOR",
        "ERROR_CORRECTION": "ERR",
        "VALIDATE_BALANCE": "VAL",
        "CONDITIONAL_TRANSFER": "CTRANS",
        "IMMUTABLE_LOG": "ILOG",
        "KEYS_GEN": "KGEN"
    }

    records = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                sym_prompt = item.get("symbolic_prompt", "")
                for k, v in compact_mapping.items():
                    sym_prompt = sym_prompt.replace(k, v)
                item["compact_symbolic_prompt"] = sym_prompt
                records.append(item)

    dictionary_overhead_tokens = 145
    total_raw_tokens = 0
    total_symbolic_tokens = 0
    domain_rows = []

    for item in records:
        domain = item.get("domain", "general")
        raw_text = item.get("raw_prompt", "")
        sym_text = item.get("compact_symbolic_prompt", "")

        raw_tokens = len(tokenizer.encode(raw_text, add_special_tokens=False))
        sym_tokens = len(tokenizer.encode(sym_text, add_special_tokens=False))

        total_raw_tokens += raw_tokens
        total_symbolic_tokens += sym_tokens

        savings = ((raw_tokens - sym_tokens) / raw_tokens) * 100 if raw_tokens > 0 else 0
        domain_rows.append(f"| `{domain}` | {raw_tokens} | {sym_tokens} | **{savings:.1f}%** |")

    net_savings_per_call = (total_raw_tokens - total_symbolic_tokens) / len(records)
    break_even_calls = dictionary_overhead_tokens / net_savings_per_call if net_savings_per_call > 0 else float('inf')

    current_date = datetime.now().strftime("%Y-%m-%d")
    
    markdown_content = f"""# Reporte de Tokenomics y Eficiencia - HEKT-NOVA v2.1 (Compact)
*Generado automáticamente el {current_date}*

Este documento detalla el análisis de compresión de tokens optimizado mediante el diccionario compacto `[H::...]`, evaluando el coste estructural y el punto de equilibrio (*break-even*) del protocolo **HEKT-NOVA**.

---

## 📊 Resumen Ejecutivo (v2.1)

* **Total de dominios evaluados:** {len(records)}
* **Tokens acumulados (Lenguaje Natural):** `{total_raw_tokens}`
* **Tokens acumulados (Simbólico Compacto):** `{total_symbolic_tokens}`
* **Ahorro neto medio por llamada:** `{net_savings_per_call:.2f} tokens`
* **Coste estructural fijo del diccionario:** `{dictionary_overhead_tokens} tokens`
* **Punto de Equilibrio (Break-Even):** **`{break_even_calls:.2f} invocaciones`**

---

## 📋 Rendimiento por Dominio

| Dominio | Tokens Naturales | Tokens Compactos | Ahorro (%) |
| :--- | :---: | :---: | :---: |
"""
    markdown_content += "\n".join(domain_rows)
    
    markdown_content += f"""

---

## 🛠️ Notas Metodológicas (Diccionario Compacto)
1. **Tokenizador Base:** `{tokenizer_name}`.
2. **Optimización Léxica:** Sustitución de namespaces extensos por acrónimos `[H::...]` para mitigar la fragmentación de subtokens en BPE.
3. **Fórmula de Break-Even:** 
   `Invocaciones = Coste Diccionario / Ahorro Neto Promedio`
"""

    os.makedirs("docs", exist_ok=True)
    output_path = "docs/tokenomics_report.md"
    
    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write(markdown_content)

    print(f"[+] Reporte exportado con éxito en: {output_path}")

if __name__ == "__main__":
    export_tokenomics_report()
