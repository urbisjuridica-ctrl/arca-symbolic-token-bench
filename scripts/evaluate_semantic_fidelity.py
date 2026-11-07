import json
import os
import requests
import torch
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as F

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME_OLLAMA = "llama3.2"

HEKT_SYSTEM_PROMPT = """Eres el núcleo de validación avanzada del protocolo HEKT-NOVA v2.1. 
Interpreta y expande estrictamente el namespace simbólico [H::...] utilizando las siguientes equivalencias operativas detalladas:
- [H::ALN] -> Alineación ontológica estricta, restricciones de seguridad estructural, coherencia de valores y gobernanza de agentes autónomos.
- [H::VRAM] -> Gestión, monitorización y optimización de memoria VRAM, asignación de tensores, control de hardware local y mitigación de desbordamientos de caché en GPU/CPU.
- [H::SEC] -> Seguridad robusta en sistemas operativos, aislamiento de procesos, sandboxing y mitigación de vulnerabilidades a nivel de kernel.
- [H::ROUT] / [H::ENR] -> Enrutamiento dinámico de agentes, optimización de flujos de mensajes asíncronos y balanceo de carga en redes distribuidas.
- [H::TEL] -> Telemetría en tiempo real, recolección de métricas de rendimiento, logging estructurado y registro de trazas de ejecución de nodos.
- [H::CTRANS] -> Transacciones asíncronas, contratos inteligentes distribuidos y validación criptográfica de estados en ledger.
- [H::TENSOR] -> Análisis avanzado de tensores, embeddings vectoriales, operaciones con PyTorch y optimización matemática de pesos.
- [H::PQC] -> Criptografía post-cuántica, algoritmos resistentes a ataques cuánticos y blindaje criptográfico de datos sensibles.

Genera una respuesta técnica, completa y detallada equivalente en profundidad a un prompt en lenguaje natural."""

def load_semantic_model():
    print("[+] Cargando modelo de embeddings para comparación semántica...")
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        return tokenizer, model
    except Exception as e:
        print(f"[!] Error al cargar el modelo de embeddings: {e}")
        return None, None

def query_ollama(prompt, use_system_prompt=False):
    payload = {
        "model": MODEL_NAME_OLLAMA,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0}
    }
    if use_system_prompt:
        payload["system"] = HEKT_SYSTEM_PROMPT

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=180)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
    except Exception as e:
        print(f"[!] Error conectando con Ollama: {e}")
    return ""

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def compute_cosine_similarity(text1, text2, tokenizer, model):
    encoded_input = tokenizer([text1, text2], padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    
    embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    embeddings = F.normalize(embeddings, p=2, dim=1)
    
    similarity = torch.sum(embeddings[0] * embeddings[1]).item()
    return similarity

def evaluate_fidelity_with_ollama():
    print("==================================================")
    print(" EVALUADOR DE FIDELIDAD SEMÁNTICA (OLLAMA) - v2.1")
    print("==================================================\n")

    dataset_path = "data/arca_symbolic_benchmark.jsonl"
    if not os.path.exists(dataset_path):
        print(f"[!] No se encontró el dataset en {dataset_path}")
        return

    tokenizer, model = load_semantic_model()
    if not tokenizer or not model:
        return

    print(f"[+] Conectando con Ollama ({MODEL_NAME_OLLAMA}) con Diccionario Refinado...\n")
    
    total_score = 0.0
    count = 0

    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                domain = item.get("domain", "general")
                raw_prompt = item.get("raw_prompt", "")
                sym_prompt = item.get("symbolic_prompt", "")

                resp_raw = query_ollama(raw_prompt, use_system_prompt=False)
                resp_sym = query_ollama(sym_prompt, use_system_prompt=True)

                if not resp_raw or not resp_sym:
                    print(f"[{domain}] ⚠️ Omitido por fallo en la respuesta de Ollama.")
                    continue

                similarity = compute_cosine_similarity(resp_raw, resp_sym, tokenizer, model)
                total_score += similarity
                count += 1

                status = "✅ Alta Fidelidad" if similarity > 0.65 else "⚠️ Revisar Deriva"
                print(f"[{domain}] Similitud de Salida: {similarity:.4f} -> {status}")

    avg_similarity = total_score / count if count > 0 else 0.0
    print("-" * 50)
    print(f"[*] Puntuación Media de Fidelidad (Diccionario Refinado): {avg_similarity:.4f}")
    print("==================================================")

if __name__ == "__main__":
    evaluate_fidelity_with_ollama()
