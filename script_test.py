import requests
import time
import csv

def tester_existence_urls(fichier_entree, fichier_sortie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"
    }

    print("--- DÉBUT DU TEST DES URLS GÉNÉRÉES ---\n")

    # Lecture du fichier d'entrée ligne par ligne
    with open(fichier_entree, mode='r', encoding='utf-8-sig', errors='ignore') as f_in, \
         open(fichier_sortie, mode='w', encoding='utf-8-sig', newline='') as f_out:

        writer = csv.writer(f_out, delimiter=';')
        writer.writerow(['url_testee', 'statut', 'code_http'])

        lignes = f_in.readlines()

        for idx, ligne in enumerate(lignes):
            url = ligne.strip().replace('"', '').replace("'", "")

            # Ignorer les lignes vides ou les en-têtes éventuels qui ne sont pas des URLs
            if not url.startswith('http'):
                continue

            statut = "À vérifier avec li_at"
            code_http = "N/A"

            try:
                # Test rapide de la réponse de la page
                response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
                code_http = response.status_code

                if response.status_code == 200:
                    statut = "EXISTE (200 OK)"
                    print(f"[{idx+1}] ✅ EXISTE : {url}")
                else:
                    print(f"[{idx+1}] ⚠️ Bloqué/Introuvable (Code {response.status_code}) : {url}")

            except Exception as e:
                statut = "Erreur de connexion"
                print(f"[{idx+1}] ❌ Erreur réseau : {url}")

            # Écriture immédiate dans le CSV de sortie
            writer.writerow([url, statut, code_http])
            f_out.flush()

            # Petite pause de 0.5 sec pour être courtois avec le serveur
            time.sleep(0.5)

    print(f"\n✅ Test terminé ! Les résultats sont enregistrés dans : '{fichier_sortie}'")

if __name__ == "__main__":
    # Mettez vos URLs directement dans url.csv
    tester_existence_urls("url.csv", "resultat_test_urls.csv")