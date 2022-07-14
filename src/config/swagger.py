template = {
    "swagger": "2.0",
    "info": {
        "title":"Bookmarks API",
        "description":"This is a sample server for a pet store.",
        "contact": {
            "respomsibleOreganisation": "",
            "respomsibleDeveloper": "",
            "url": "http://www.twitter.com/support",
            "email": "aliyutimileyin2340@gmail.com"
        },
        "name": "Apache 2.0",
        "termsOfService": "http://www.twitter.com/support",  
        "version": "1.0"    
    },

    "basePath": "/api/v1", #urls
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinations": {  #api use beareer token
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example \"Authorization Bearer {token}\""
        }
    }
}

swagger_config = {
    "headers": [        
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec/json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True
        }
    ],
    "static_url_path": "/flasgger_static",
    "static_ui": True,
    "specs_route": "/"
}