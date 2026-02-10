import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from bs4 import BeautifulSoup

async def scrape_la_centrale(modele_auto):
    async with async_playwright() as p:
        # On lance le navigateur
        browser = await p.chromium.launch(headless=True)
        
        # On crée un contexte avec un User-Agent de vrai humain
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        
        page = await context.new_page()
        # On applique le mode furtif (Stealth)
        await stealth_async(page)
        
        # URL de recherche (exemple sur La Centrale)
        # On encode la recherche pour que les espaces deviennent des %20
        search_query = modele_auto.replace(' ', '%20')
        url = f"https://www.lacentrale.fr/listing?options=&q={search_query}"
        
        print(f"🔍 Analyse du marché pour : {modele_auto}...")
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # On attend que les annonces chargent
            await page.wait_for_selector('.SearchResult_resultCard')
            
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            offres = []
            # Sélecteurs mis à jour pour La Centrale (peuvent varier)
            annonces = soup.find_all('div', class_='SearchResult_resultCard')
            
            for i, annonce in enumerate(annonces):
                try:
                    # Extraction du prix
                    prix_text = annonce.select_one('.Price_price').text
                    prix = int(''.join(filter(str.isdigit, prix_text)))
                    
                    # Extraction du kilométrage
                    # Souvent dans une liste de caractéristiques
                    caracs = annonce.select('.Characteristics_characteristic')
                    km_text = caracs[1].text # Le 2ème élément est souvent le kilométrage
                    km = int(''.join(filter(str.isdigit, km_text)))
                    
                    # Extraction de l'année
                    annee = int(caracs[0].text)
                    
                    offres.append({'prix': prix, 'km': km, 'annee': annee})
                except Exception as e:
                    continue
            
            await browser.close()
            print(f"✅ {len(offres)} offres trouvées sur le marché.")
            return offres

        except Exception as e:
            print(f"❌ Erreur de connexion (Bot détecté ou timeout) : {e}")
            await browser.close()
            return []

# Test du script
# asyncio.run(scrape_la_centrale("Golf 7 2018"))
