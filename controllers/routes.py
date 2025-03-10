from flask import render_template, request, redirect, url_for
# Essa biblioteca serve para ler uma determinada URL
import urllib
# Converte dados para o formato json
import json

treinadores = []

pokemonlist = [{'nome': 'Pikachu',
             'tipo': 'elétrico'}]


def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/pokemons', methods=['GET', 'POST'])
    def pokemons():
        pokemon = pokemonlist[0]
        if request.method == 'POST':
            if request.form.get('treinador'):
                treinadores.append(request.form.get('treinador'))
                return redirect(url_for('pokemons'))

        return render_template('pokemons.html', pokemon=pokemon, treinadores=treinadores)

    @app.route('/cadpokemon', methods=['GET', 'POST'])
    def cadpokemon():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            pokemonlist.append(form_data)
            return (redirect(url_for('cadpokemon')))
        return render_template('cadpokemon.html', pokemonlist=pokemonlist)

    @app.route('/apipokemon', methods=['GET', 'POST'])
    @app.route('/apipokemon/<string:nome>', methods=['GET', 'POST'])
    def apipokemons(nome=None):
        url = 'https://pokeapi.co/api/v2/pokemon?limit=100'
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

