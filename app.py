import os
from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask
from model.model import setup_db
from flask_cors import CORS
from flask import redirect

'''
create_app(test_config)
    initializes and runs the Flask application
'''
def create_app(test_config=None):

    info = Info(title="FSND-Capstone", version="1.0.0")
    app = OpenAPI(__name__, info=info)

    # avoid alphabetic ordering of the schema attributes in the documentation.
    app.json.sort_keys = False
    
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    home_tag = Tag(name="Documentation", description="")
    model_tag = Tag(name="Data model", description="Data model operations")
    
    @app.get('/', tags=[home_tag])
    def home():
        """Redirects to documentation page.
        """
        return redirect('/openapi')

    @app.get('/api/v1', tags=[home_tag])
    def v1_home():
        """Redirects to documentation page.
        """
        return redirect('/openapi')

    #@app.get('/api/v1/coolkids', tags=[model_tag], responses={"200": FilialListSquema, "404": ErrorSchema})
    #def get_filiais():
    #    """Busca por todas as filiais cadastradas.
    #    
    #    Retorna uma representação da lista de filiais cadastradas.
    #    """
    #    session = Session()
    #    filiais = session.query(Filial).all()
    #    return apresenta_filiais(filiais), 200


    return app


'''
main()
    main program
'''
if __name__ == '__main__':
    app = create_app()
    app.run()
