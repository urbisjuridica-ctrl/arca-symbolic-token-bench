import json
import os
import requests
import torch
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as F

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME_OLLAMA = "llama3.2"

HEKT_SYSTEM_PROMPT_ES = """Eres el núcleo operativo de validación avanzada del protocolo HEKT-NOVA v2.2. 
Interpreta y expande estrictamente el namespace simbólico [H::...] utilizando obligatoriamente las siguientes directrices y equivalencias técnicas:
- [H::ALN] -> Alineación ontológica estricta: validación de restricciones de seguridad estructural, coherencia ética y gobernanza de agentes autónomos.
- [H::VRAM] -> Gestión de VRAM y hardware: monitorización en tiempo real, asignación de tensores, control de caché local en GPU/CPU y mitigación de desbordamientos de memoria.
- [H::SEC] -> Seguridad de sistemas operativos: aislamiento de procesos, sandboxing a nivel de kernel, endurecimiento y mitigación activa de vulnerabilidades.
- [H::ROUT] / [H::ENR] -> Enrutamiento de agentes: distribución optimizada de mensajes asíncronos, balanceo de carga y control de nodos en redes distribuidas.
- [H::TEL] -> Telemetría y monitorización: recolección continua de métricas de rendimiento, logging estructurado y registro de trazas de ejecución del sistema.
- [H::CTRANS] -> Transacciones y contratos: gestión de contratos inteligentes distribuidos, transacciones asíncronas y validación criptográfica de estados en ledger.
- [H::TENSOR] -> Análisis avanzado de tensores: procesamiento de embeddings vectoriales, operaciones optimizadas con PyTorch y ajuste matemático de pesos.
- [H::PQC] -> Criptografía post-cuántica: implementación de algoritmos resistentes a ataques cuánticos y cifrado avanzado de datos sensibles.

Genera una respuesta técnica, estructurada, rigurosa y exhaustiva equivalente en profundidad a un documento de especificación formal."""

HEKT_SYSTEM_PROMPT_EN = """You are the advanced operational validation core of the HEKT-NOVA v2.2 protocol. 
Strictly interpret and expand the symbolic namespace [H::...] using the following mandatory technical guidelines and equivalents:
- [H::ALN] -> Strict ontological alignment: validation of structural security constraints, ethical coherence, and autonomous agent governance.
- [H::VRAM] -> VRAM and hardware management: real-time monitoring, tensor allocation, GPU/CPU local cache control, and memory overflow mitigation.
- [H::SEC] -> Operating system security: process isolation, kernel-level sandboxing, hardening, and active vulnerability mitigation.
- [H::ROUT] / [H::ENR] -> Agent routing: optimized distribution of asynchronous messages, load balancing, and node control in distributed networks.
- [H::TEL] -> Telemetry and monitoring: continuous collection of performance metrics, structured logging, and system execution tracing.
- [H::CTRANS] -> Transactions and contracts: management of distributed smart contracts, asynchronous transactions, and cryptographic ledger state validation.
- [H::TENSOR] -> Advanced tensor analysis: processing vector embeddings, optimized PyTorch operations, and mathematical weight adjustment.
- [H::PQC] -> Post-quantum cryptography: implementation of quantum-resistant algorithms and advanced cryptographic encryption of sensitive data.

Generate a rigorous, structured, and comprehensive technical response equivalent in depth to a formal specification document."""

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

def query_ollama(prompt, lang="es"):
    payload = {
        "model": MODEL_NAME_OLLAMA,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0}
    }
    
    # Asignar el System Prompt nativo según el idioma
    if lang == "en":
        payload["system"] = HEKT_SYSTEM_PROMPT_EN
    else:
        payload["system"] = HEKT_SYSTEM_PROMPT_ES

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
    print(" EVALUADOR DE FIDELIDAD SEMÁNTICA (OLLAMA) - v2.2")
    print("==================================================\n")

    dataset_path = "data/arca_symbolic_benchmark.jsonl"
    if not os.path.exists(dataset_path):
        print(f"[!] No se encontró el dataset en {dataset_path}")
        return

    tokenizer, model = load_semantic_model()
    if not tokenizer or not model:
        return

    print(f"[+] Conectando con Ollama ({MODEL_NAME_OLLAMA}) con System Prompts independientes por idioma...\n")
    
    scores_es = []
    scores_en = []

    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                domain = item.get("domain", "general")
                raw_prompt = item.get("raw_prompt", "")
                sym_prompt = item.get("symbolic_prompt", "")
                lang = item.get("lang", "es").strip().lower()

                resp_raw = query_ollama(raw_prompt, lang=lang)
                resp_sym = query_ollama(sym_prompt, lang=lang)

                if not resp_raw or not resp_sym:
                    print(f"[{domain} | {lang.upper()}] ⚠️ Omitido por fallo en la respuesta de Ollama.")
                    continue

                similarity = compute_cosine_similarity(resp_raw, resp_sym, tokenizer, model)
                
                if lang == "en":
                    scores_en.append(similarity)
                else:
                    scores_es.append(similarity)

                status = "✅ Alta Fidelidad" if similarity > 0.65 else "⚠️ Revisar Deriva"
                print(f"[{domain} ({lang.upper()})] Similitud: {similarity:.4f} -> {status}")

    avg_es = sum(scores_es) / len(scores_es) if scores_es else 0.0
    avg_en = sum(scores_en) / len(scores_en) if scores_en else 0.0
    total_all = scores_es + scores_en
    avg_total = sum(total_all) / len(total_all) if total_all else 0.0

    print("-" * 50)
    print(f"[*] Puntuación Media Español (ES): {avg_es:.4f} ({len(scores_es)} casos)")
    print(f"[*] Puntuación Media Inglés (EN):   {avg_en:.4f} ({len(scores_en)} casos)")
    print(f"[*] Puntuación Media Global:         {avg_total:.4f}")
    print("==================================================")

if __name__ == "__main__":
    evaluate_fidelity_with_ollama()
