from flask import render_template, request, redirect, url_for
import urllib # Essa biblioteca serve para ler uma determinada URL
import json
from models.database import db, Pokemon

trainers = []

pokemonlist = [{'nome': 'Pikachu',
             'tipo': 'elétrico'}]


def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/treinadores', methods=['GET', 'POST'])
    def treinadores():
        pokemon = pokemonlist[0]
        if request.method == 'POST':
            if request.form.get('treinador'):
                trainers.append(request.form.get('treinador'))
                return redirect(url_for('treinadores'))

        return render_template('treinadores.html', pokemon=pokemon, trainers=trainers)

    @app.route('/pokemons', methods=['GET', 'POST'])
    @app.route('/pokemons/delete/<int:id>')
    def pokemons(id=None):
        if id:
            pokemon = Pokemon.query.get(id)
            db.session.delete(pokemon)
            db.session.commit()
            return redirect(url_for('pokemons'))
        
        if request.method == 'POST':
            newpokemon = Pokemon(request.form['nome'], request.form['tipo'])
            db.session.add(newpokemon)
            db.session.commit()
            return redirect(url_for('pokemons'))
        else:   
            page = request.args.get('page', 1, type=int)
            per_page = 3
            pokemon_page = Pokemon.query.paginate(page=page, per_page=per_page)
            return render_template('pokemons.html', pokemonlist=pokemon_page)

    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        p = Pokemon.query.get(id)

        if request.method == 'POST':
            p.nome = request.form['nome']
            p.tipo = request.form['tipo']
            db.session.commit()
            return redirect(url_for('pokemons'))
        return render_template('editpokemon.html', p=p)

    @app.route('/apipokemon', methods=['GET', 'POST'])
    @app.route('/apipokemon/<string:nome>', methods=['GET', 'POST'])
    def apipokemons(nome=None):
        url = 'https://pokeapi.co/api/v2/pokemon?limit=10'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)

        if res.getcode() != 200:
            return f'Erro ao acessar PokeAPI: {response.getcode()}'

        data = res.read()
        pokemonsjson = json.loads(data)

        for pokemon in pokemonsjson['results']:
            req = urllib.request.Request(pokemon['url'], headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req)

            pokemon_data = json.loads(res.read())
            pokemon['id'] = pokemon_data['id']
            pokemon['height'] = pokemon_data['height']
            pokemon['abilities'] = [ability['ability']['name'] for ability in pokemon_data['abilities']]
            pokemon['types'] = [type_info['type']['name'] for type_info in pokemon_data['types']]
            pokemon['sprite'] = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_data['id']}.png"
            pokemon['sprite_shiny'] = pokemon_data['sprites']['front_shiny']

        if nome:
            pinfo = []
            for p in pokemonsjson['results']:
                if p['name'] == nome:
                    pinfo = p
                    break
            if pinfo:
                return render_template('pokemoninfo.html', pinfo=pinfo)
            else:
                return f'Pokemon com o nome {nome} não foi encontrado.'

        return render_template('apipokemons.html',
                               pokemonsjson=pokemonsjson['results'])

