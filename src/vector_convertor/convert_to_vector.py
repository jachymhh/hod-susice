import pdfplumber
import os
import glob
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import torch # Přidáme knihovnu torch pro detekci zařízení

# --- KONFIGURACE ---
VSTUPNI_SLOZKA = './'  # ZDE NAHRADIT SKUTEČNOU CESTOU
VYSTUPNI_SLOZKA = './converted_vectors' # ZDE NAHRADIT SKUTEČNOU CESTOU
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2' 
CHUNK_SIZE = 500  
CHUNK_OVERLAP = 50 

# KLÍČOVÁ ZMĚNA: Vynucení CPU zařízení
# Detekce zařízení: Pokud je CUDA dostupná, ale má nekompatibilní verzi,
# vynutíme použití 'cpu', abychom předešli chybě kernelu.
DEVICE = 'cpu' 
print(f"Generování vektorů bude probíhat na zařízení: {DEVICE}")

# --- (Funkce rozdel_text_na_bloky zůstává beze změny) ---
def rozdel_text_na_bloky(text, velikost_bloku, prekryti):
    """Rozdělí dlouhý text na menší bloky (chunks) s překrytím."""
    if not text:
        return []
    
    bloky = []
    start = 0
    while start < len(text):
        end = start + velikost_bloku
        blok = text[start:end]
        bloky.append(blok)
        start += velikost_bloku - prekryti
        if end >= len(text):
            break
    return bloky


def preved_slozku_pdf_na_vektory(vstupni_slozka, vystupni_slozka, model_name):
    
    if not os.path.exists(vystupni_slozka):
        os.makedirs(vystupni_slozka)
        
    # 2. Načtení modelu a PŘEDÁNÍ DEVICE
    print(f"Načítám Sentence Transformer model: {model_name}...")
    # Nyní model inicializujeme s explicitním zařízením
    model = SentenceTransformer(model_name, device=DEVICE) 
    
    # ... (Zbytek kódu pro hledání PDF zůstává beze změny) ...
    cesty_k_pdf_souborum = glob.glob(os.path.join(vstupni_slozka, "*.pdf"))
    if not cesty_k_pdf_souborum:
        print(f"Nenalezeny žádné PDF soubory ve složce: {vstupni_slozka}")
        return

    vsechny_vektory = []
    metadata_bloku = []
    
    # 4. Iterace a zpracování
    for cesta_pdf in cesty_k_pdf_souborum:
        nazev_souboru = os.path.basename(cesta_pdf)
        print(f"\n--- Zpracovávám soubor: {nazev_souboru} ---")
        
        try:
            # a) Extrakce textu z PDF
            with pdfplumber.open(cesta_pdf) as pdf:
                plny_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

            # b) Rozdělení textu na bloky
            textove_bloky = rozdel_text_na_bloky(plny_text, CHUNK_SIZE, CHUNK_OVERLAP)
            print(f"Text rozdělen na {len(textove_bloky)} bloků.")
            
            # c) Generování vektorů (embeddings)
            if textove_bloky:
                # model.encode nyní automaticky použije 'cpu'
                vektory = model.encode(textove_bloky, convert_to_numpy=True)
                
                # d) Sběr vektorů a metadat
                vsechny_vektory.append(vektory)
                
                for i, blok in enumerate(textove_bloky):
                    metadata_bloku.append({
                        "id": f"{nazev_souboru}_{i}",
                        "zdroj": nazev_souboru,
                        "blok_textu": blok,
                        "index_bloku": i
                    })
                
                print(f"  Úspěšně vygenerováno {len(vektory)} vektorů.")

        except Exception as e:
            print(f"  CHYBA při zpracování souboru {nazev_souboru}: {e}")

    # ... (Zbytek kódu pro ukládání výsledků zůstává beze změny) ...
    if vsechny_vektory:
        finalni_vektory = np.concatenate(vsechny_vektory, axis=0)
        
        cesta_vektory = os.path.join(vystupni_slozka, "dokumenty_vektory.npy")
        np.save(cesta_vektory, finalni_vektory)
        
        cesta_metadata = os.path.join(vystupni_slozka, "dokumenty_metadata.json")
        with open(cesta_metadata, 'w', encoding='utf-8') as f:
            json.dump(metadata_bloku, f, ensure_ascii=False, indent=4)
        
        print("\n" + "="*70)
        print(f"Vektory i metadata úspěšně uloženy!")
        print(f"Vektory (NumPy matice): {cesta_vektory} (tvar: {finalni_vektory.shape})")
        print(f"Metadata (JSON): {cesta_metadata} (celkem {len(metadata_bloku)} bloků)")
        print("="*70)

# --- SPUŠTĚNÍ ---
preved_slozku_pdf_na_vektory(VSTUPNI_SLOZKA, VYSTUPNI_SLOZKA, EMBEDDING_MODEL_NAME)
