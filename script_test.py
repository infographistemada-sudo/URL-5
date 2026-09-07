import requests
import time
import csv
import random

def tester_existence_urls_github(fichier_entree, fichier_sortie):
    # Liste de User-Agents pour ne pas toujours envoyer la même signature
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
    ]

    print("--- DÉBUT DU TEST ADAPTÉ À GITHUB ACTIONS ---\n")

    with open(fichier_entree, mode='r', encoding='utf-8-sig', errors='ignore') as f_in, \
         open(fichier_sortie, mode='w', encoding='utf-8-sig', newline='') as f_out:

        writer = csv.writer(f_out, delimiter=';')
        writer.writerow(['url_testee', 'statut', 'code_http'])

        for idx, ligne in enumerate(f_in):
            ligne_propre = ligne.strip()
            
            # --- NETTOYAGE : Si la ligne contient du texte après un ';', on ne garde que l'URL ---
            url = ligne_propre.split(';')[0].strip().replace('"', '').replace("'", "")

            if not url.startswith('http'):
                continue

            # Choix d'un User-Agent aléatoire
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"
            }

            statut = "À vérifier avec li_at"
            code_http = "N/A"

            try:
                response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
                code_http = response.status_code

                if response.status_code == 200:
                    statut = "EXISTE (200 OK)"
                    print(f"[{idx+1}] ✅ EXISTE : {url}")
                elif response.status_code == 429:
                    statut = "Bloqué 429 (Trop de requêtes)"
                    print(f"[{idx+1}] 🛑 Bloqué 429 par LinkedIn. Pause forcing de 15 secondes...")
                    time.sleep(15) # Pause de sécurité si LinkedIn commence à bloquer
                else:
                    print(f"[{idx+1}] ⚠️ Code {response.status_code} : {url}")

            except Exception as e:
                statut = "Erreur de connexion"
                print(f"[{idx+1}] ❌ Erreur : {url}")

            writer.writerow([url, statut, code_http])
            f_out.flush()

            # PAUSE OBLIGATOIRE sur GitHub : entre 2.5 et 4.5 secondes au hasard
            time.sleep(random.uniform(2.5, 4.5))

    print(f"\n✅ Test terminé ! Fichier enregistré : '{fichier_sortie}'")

if __name__ == "__main__":
    tester_existence_urls_github("url.csv", "resultat_test_urls.csv")