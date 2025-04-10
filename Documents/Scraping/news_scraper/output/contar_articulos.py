import json
from collections import defaultdict

def contar_urls_unicas_por_fuente(path_jsonl):
    urls_por_fuente = defaultdict(set)

    with open(path_jsonl, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                item = json.loads(linea)
                fuente = item.get("source", "Desconocido")
                url = item.get("url")
                if url:
                    urls_por_fuente[fuente].add(url)

    total = sum(len(urls) for urls in urls_por_fuente.values())
    print(f"📊 Total de URLs únicas: {total}\n")
    print("📰 URLs únicas por fuente:")
    for fuente, urls in urls_por_fuente.items():
        print(f"• {fuente}: {len(urls)}")

if __name__ == "__main__":
    contar_urls_unicas_por_fuente("articles_final.jsonl")
