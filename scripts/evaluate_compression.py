import json
import os
from transformers import AutoTokenizer

def evaluate_dataset():
    # Cargar tokenizador de referencia estándar
    print("Cargando tokenizador de referencia (Llama 3)...")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
    
    input_path = "data/arca_symbolic_benchmark.jsonl"
    
    if not os.path.exists(input_path):
        print(f"Error: No se encuentra el archivo en {input_path}")
        return

    print(f"Procesando registros desde {input_path}...\n")
    
    total_raw_tokens = 0
    total_symbolic_tokens = 0
    
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            
            # Recalcular tokens con el tokenizador activo
            raw_tokens = len(tokenizer.encode(record["raw_prompt"]))
            symbolic_tokens = len(tokenizer.encode(record["symbolic_prompt"]))
            compression_ratio = round(1 - (symbolic_tokens / raw_tokens), 3)
            
            total_raw_tokens += raw_tokens
            total_symbolic_tokens += symbolic_tokens
            
            print(f"[{record['id']}] Dominio: {record['domain']}")
            print(f"  - Tokens Naturales:  {raw_tokens}")
            print(f"  - Tokens Simbólicos: {symbolic_tokens}")
            print(f"  - Compresión Real:   {compression_ratio * 100:.1f}%\n")
            
    global_compression = round(1 - (total_symbolic_tokens / total_raw_tokens), 3)
    print("=" * 40)
    print(f"RESUMEN GLOBAL DE COMPRESIÓN HEKT-NOVA:")
    print(f"  - Total Tokens Naturales:  {total_raw_tokens}")
    print(f"  - Total Tokens Simbólicos: {total_symbolic_tokens}")
    print(f"  - Eficiencia Global:       {global_compression * 100:.1f}% de ahorro")
    print("=" * 40)

if __name__ == "__main__":
    evaluate_dataset()

