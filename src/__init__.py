
from flask import Flask, jsonify, redirect
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db, Bookmark
from flask_jwt_extended import JWTManager
import sys
from flasgger import Swagger, swag_from
from src.config.swagger import template,swagger_config 



def create_app(test_config=None):

    app = Flask(__name__,
    instance_relative_config=True)

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY= os.environ.get('JWT_SECRET_KEY'),


            SWAGGER={
                'title':"Bookmarks API",'uiversion': 3
            }
        )


            
    else:
         app.config.from_mapping(test_config)  


    db.app = app
    db.init_app(app)
#based on secret_key decrypt and encrypt .flaskenv file for more info
    JWTManager(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    Swagger(app, config=swagger_config, template=template)
#to keep track of the visits on link. we take the shorturl since thats what the user will be visiting.

    
    @app.route('/')
    def hello():
        return 'Hello World!'
 

    app.get('/<short_url>')
    @swag_from("./docs/short_url.yaml")
    def redirect_to_url(short_url):
        error= False
        try:
            bookmark = Bookmark.query.filter_by(short_url=short_url).first()

            if bookmark is not None:
                bookmark.visits = bookmark.visits + 1
                db.session.commit()

                return redirect(bookmark.url)
        except:
            error = True
            print(sys.exc_info)




    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Server error'
        }), 500


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400




    return app


