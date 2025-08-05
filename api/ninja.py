from ninja import NinjaAPI
from ninja_simple_jwt.auth.views.api import mobile_auth_router, web_auth_router

# Création de l'instance principale de l'API Ninja.
# Cette instance gère toutes les routes de l'API et génère la documentation interactive.
api = NinjaAPI(title="Pokemon API", version="1.0")

# Ajout des sous-routes à l'API.
# Chaque sous-route correspond à un module qui gère un ensemble d'endpoints spécifiques.

api.add_router("/basics/", "api.basics.router")         # Endpoints de base (ex : addition, test API)
# disponible sur http://localhost:8000/api/basics/
api.add_router("/pokemon/", "api.pokemon.router")       # Endpoints pour manipuler les Pokémon (vue, liste, etc.)
# disponible sur http://localhost:8000/api/pokemon/
api.add_router("/querysets/", "api.querysets.router")   # Endpoints pour manipuler des ensembles de données
# disponible sur http://localhost:8000/api/querysets/
api.add_router("/type/", "api.type.router")             # Endpoints pour les types de Pokémon (création, édition, etc.)
# disponible sur http://localhost:8000/api/type/
api.add_router("/auth/", "api.authentification.router")   # Endpoints pour l'authentification (clé API, basic auth)
# disponible sur http://localhost:8000/api/auth/
api.add_router("/auth/mobile/", mobile_auth_router)     # Endpoints pour l'authentification JWT mobile
# disponible sur http://localhost:8000/api/auth/mobile/
api.add_router("/auth/web/", web_auth_router)           # Endpoints pour l'authentification JWT web
# disponible sur http://localhost:8000/api/auth/web/

# Grâce à cette organisation, chaque fonctionnalité de l'API est séparée dans un fichier dédié,
# ce qui rend le projet plus clair, évolutif et facile à maintenir.
# La documentation interactive de l'API est accessible à l'URL /api/docs