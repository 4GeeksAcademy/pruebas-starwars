import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, Users, Products, Bills, BillItems, Followers, Posts, Coments, Medias, Planets, PlanetFavourite, Characters, CharacterFavourites

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Añadir modelos al panel de administración
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Products, db.session))
    admin.add_view(ModelView(Bills, db.session))
    admin.add_view(ModelView(BillItems, db.session))
    admin.add_view(ModelView(Followers, db.session))  
    admin.add_view(ModelView(Posts, db.session))  
    admin.add_view(ModelView(Coments, db.session)) 
    admin.add_view(ModelView(Medias, db.session))  
    admin.add_view(ModelView(Planets, db.session)) 
    admin.add_view(ModelView(PlanetFavourite, db.session)) 
    admin.add_view(ModelView(Characters, db.session)) 
    admin.add_view(ModelView(CharacterFavourites, db.session)) 