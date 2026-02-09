def juger_offre(prix_utilisateur, km_utilisateur, base_donnees):
    # On filtre la BDD pour ne garder que les voitures proches en kilométrage (+/- 15%)
    similaires = [o['prix'] for o in base_donnees 
                  if km_utilisateur * 0.85 <= o['km'] <= km_utilisateur * 1.15]
    
    if not similaires:
        return "Pas assez de données pour comparer !"

    prix_moyen = sum(similaires) / len(similaires)
    difference = ((prix_utilisateur - prix_moyen) / prix_moyen) * 100

    if difference < -10:
        return "🔥 EXCELLENTE OFFRE. C'est presque suspect, vérifie le châssis !"
    elif difference < 5:
        return "✅ Offre honnête. C'est le prix du marché."
    elif difference < 15:
        return "⚠️ Un peu cher. Essaie de négocier au moins 1000€."
    else:
        return "💩 C'est de la merde. Le vendeur te prend pour un pigeon."