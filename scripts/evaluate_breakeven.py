import json
import os
from transformers import AutoTokenizer

def evaluate_tokenomics():
    print("[+] Ejecutando evaluación de tokenomics con diccionario compacto HEKT-NOVA v2.1...")

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

    # Mapeo de compactación léxica para reducir subtokens BPE
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
                # Aplicar sustitución compacta al prompt simbólico si existe
                sym_prompt = item.get("symbolic_prompt", "")
                for k, v in compact_mapping.items():
                    sym_prompt = sym_prompt.replace(k, v)
                item["compact_symbolic_prompt"] = sym_prompt
                records.append(item)

    dictionary_overhead = 145
    total_raw = 0
    total_sym = 0

    print("\n" + "="*70)
    print(f"{'DOMINIO':<25} | {'NATURAL':<8} | {'COMPACTO':<8} | {'AHORRO (%)':<10}")
    print("="*70)

    for item in records:
        domain = item.get("domain", "general")
        raw_text = item.get("raw_prompt", "")
        sym_text = item.get("compact_symbolic_prompt", "")

        raw_tokens = len(tokenizer.encode(raw_text, add_special_tokens=False))
        sym_tokens = len(tokenizer.encode(sym_text, add_special_tokens=False))

        total_raw += raw_tokens
        total_sym += sym_tokens

        savings_pct = ((raw_tokens - sym_tokens) / raw_tokens) * 100 if raw_tokens > 0 else 0
        print(f"{domain:<25} | {raw_tokens:<8} | {sym_tokens:<8} | {savings_pct:>6.1f}%     ")

    print("="*70)
    net_savings = (total_raw - total_sym) / len(records)
    breakeven = dictionary_overhead / net_savings if net_savings > 0 else float('inf')

    print(f"\n[RESUMEN GLOBAL]")
    print(f" - Tokens totales naturales  : {total_raw}")
    print(f" - Tokens totales compactos  : {total_sym}")
    print(f" - Ahorro medio por llamada  : {net_savings:.2f} tokens")
    print(f" - Punto de equilibrio (BE)  : ~{breakeven:.1f} llamadas\n")

if __name__ == "__main__":
    evaluate_tokenomics()
