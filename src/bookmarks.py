
from flask import Blueprint, request, jsonify, redirect
import validators   
from src.database import Bookmark,db
from flask_jwt_extended import get_jwt_identity, jwt_required
import sys
from flasgger import swag_from


bookmarks= Blueprint("bookmarks",__name__,url_prefix="/api/v1/bookmarks" )

# register user
@bookmarks.route('/', methods = ['POST', 'GET'])

@jwt_required()
@swag_from("./docs/bookmarks/post.yaml")
def handle_bookmark():
    current_user=get_jwt_identity()  #to post in bookmark we need current user
    if request.method == 'POST':

        data = request.get_json()
        body = data.get('body', '')
        url = data.get('url', '')

        if not validators.url(url):
            return jsonify({
                'error': 'link required'
            }), 400

        if Bookmark.query.filter_by(url = url).first():
            return jsonify({'error': 'link exist'}), 409



        bookmark=Bookmark(url = url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visits': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
        }), 201

    else:
        #pagination

        page = request.args.get('page', 1, type =int)
        per_page = request.args.get('per_page', 5, type=int)
#sending back all, make query first, getting the book!!

        bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)

        # serialize, to get the bookmarks each each, because we wont be able to get the object, so we get them in a list
        data = []

        for bookmark in bookmarks.items:
            data.append({
                'id': bookmark.id,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visits': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at
            })
#tell frontend there are other pages, current page
# all these are default values of pagination. 
        meta = {
            "page": bookmarks.page,
            "pages": bookmarks.pages,
            "total_count": bookmarks.total,
            "prev": bookmarks.prev_num,
            "next": bookmarks.next_num,
            "has_prev": bookmarks.has_prev,
            "has_next": bookmarks.has_next
        }
#Note: after pagination, our value get sent back to us in key, value pairs, so you would need to loop through the object with .itms i.e your query.

# to get page ?page=1 you need more ?page=1&per_page=11
# having key as data and returning data
        return jsonify({'data':data, 'meta': meta}), 200

#get user

@bookmarks.get('/<int:id>')
@jwt_required()
def get_book(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({'message': 'item not found'}), 404


    return jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visits': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at
    }), 200


@bookmarks.route('edit/<int:id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_book(id):
    current_user = get_jwt_identity()

    data = request.get_json()
    body = data.get('body', '')
    url = data.get('url', '')
#we find the bookmark

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
    

    if not bookmark:
        return jsonify({'message': 'item not found'}), 404

    bookmark.url = url
    bookmark.body = body

#no need to add, just commit
    db.session.commit()
#we  need to return
    return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visits': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
    })

@bookmarks.route('delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({'message': 'item not found'}), 404

    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({
        'message': 'Deleted'
    }), 204


@bookmarks.get("/stats")
@jwt_required()
@swag_from("./docs/bookmarks/stats.yaml")
def get_stats():
    current_user = get_jwt_identity()
    data =[]

    items = Bookmark.query.filter_by(user_id=current_user).all()
    
    for item in items:
        new_link = {
            'visits': item.visits,
            'url': item.url,
            'id': item.id,
            'short_url': item.short_url
        }

        data.append(new_link)

    return jsonify({'data':data}), 200




# bookmarks.get('/<short_url>')
# @jwt_required()
# def redirect_to_url(short_url):

#     error= False
#     try:
#         bookmark = Bookmark.query.filter_by(short_url=short_url).first()

#         if bookmark is not None:
#             bookmark.visits = bookmark.visits + 1
#             db.session.commit()

#             return redirect(bookmark.url)
#     except:
#         error = True
#         print(sys.exc_info)
#when user checks link
 