from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Clé secrète pour gérer la session

# Produits disponibles (simples exemples)
produits = {
    1: {"nom": "Ordinateur", "prix": 70000,"image":"images/mac.jpg"},
    2: {"nom": "Smartphone", "prix": 30000,"image":"images/smart.jpg"},
    3: {"nom": "Casque Bluetooth", "prix": 5000,"image":"images/casque.jpg"}
}

# Route principale : Affichage des produits
@app.route('/')
def index():
    return render_template('index.html', produits=produits)

# Ajouter un produit au panier
@app.route('/ajouter/<int:produit_id>')
def ajouter_au_panier(produit_id):
    if 'panier' not in session:
        session['panier'] = {}

    panier = session['panier']

    if str(produit_id) in panier:
        panier[str(produit_id)] += 1
    else:
        panier[str(produit_id)] = 1

    session['panier'] = panier
    return redirect(url_for('index'))

# Voir le panier
@app.route('/panier')
def afficher_panier():
    panier = session.get('panier', {})
    
    # Correction ici 🔥
    contenu_panier = {
        int(k): {'nom': produits[int(k)]['nom'], 'prix': produits[int(k)]['prix'], 'quantité': v} 
        for k, v in panier.items() if int(k) in produits
    }
  

    total = sum(produits[int(k)]['prix'] * v for k, v in panier.items() if int(k) in produits)

    return render_template('panier.html', panier=contenu_panier, total=total)

# Supprimer un produit du panier
@app.route('/supprimer/<int:produit_id>')
def supprimer_du_panier(produit_id):
    panier = session.get('panier', {})

    if str(produit_id) in panier:
        del panier[str(produit_id)]

    session['panier'] = panier
    return redirect(url_for('afficher_panier'))

# Vider le panier
@app.route('/vider')
def vider_panier():
    session['panier'] = {}
    return redirect(url_for('afficher_panier'))

if __name__ == '__main__':
    app.run(debug=True)
