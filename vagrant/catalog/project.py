from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash, jsonify
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from models import Catalog, Base, Item, User

from datetime import datetime

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Establish all conversation with the database


engine = create_engine('sqlite:///legocatalog.db', pool_pre_ping=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Load the user information for OAuth2.0 for Google


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Create anti-forgery state token


@app.route('/login')
def showLogin():
    """
    Behavior:
        Creates an anti-forgery state token for the user identification with
        OAuth2.0 solution providers
    Args:
        None
    Returns:
        state - a 32 character random ascii string
        Call Flask render_template() function for the login.html page, passing
        the component state.
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# Google OAuth2.0 connect


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Behavior:
        Connect to the Google OAuth2 api to identify and connect the user
        Add the user details to login_session
    Args:
        None
    Returns:
        response - text string in a json format
        output - html code
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                    'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # noqa
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    """
    Behavior:
        Add a user to the User table
    Args:
        login_session - a list of user details
    Returns:
        user.id - integer, the ID of the created user
    """
    newUser = User(
        Uname=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
        )
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
        email=login_session['email']).one_or_none()
    return user.id


def getUserInfo(user_id):
    """
    Behavior:
        Collect user details based on ID
    Args:
        user_id - integer
    Returns:
        user - dict, contains the user tables as stored in the User table
    """
    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


def getUserID(email):
    """
    Behavior:
        Collect the user id based on the user email
    Args:
        email - text string
    Returns:
        user.id - integer, the ID of the created user
    """
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except:
        return None

# Google disconnect functions


@app.route('/gdisconnect')
def gdisconnect():
    """
    Behavior:
        Connect to the Google OAuth2 api to disconnect the user
    Args:
        None
    Returns:
        response - text string in a json format
    """
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    response_body = h.request(url, 'GET')[1]
    if result['status'] == '200':
        response = make_response(json.dumps(
            'Successfully disconnected. Message: %s' % response_body), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user. Message: %s'
            % response_body), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    """
    Behavior:
        Remove the user details from login_session
    Args:
        None
    Returns:
        flask flash message
        Redirect to ShowMain function
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showMain'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showMain'))

# Application pages


@app.route('/')
@app.route('/catalog/', methods=['GET', 'POST'])
def showMain():
    """
    Behavior:
        Query the Catalog and Item tables
        Load catalog_summary.html
    Args:
        None
    Returns:
        body_set - dict, contains the catalog details
        latest_item - dict, contains the 8 latest added items details
        Call Flask render_template() function for the catalog_summary.html
        page, passing the component body_set and latest_item.
    """
    body_set = session.query(Catalog).all()
    latest_item = session.query(
        Item.Iname, Item.created_at,
        Catalog.Cname, Item.item_image).join(
        Catalog).order_by(desc(Item.created_at)).limit(8)
    return render_template(
        'catalog_summary.html', body_set=body_set,
        latest_item=latest_item
        )


@app.route('/catalog/<string:catalog_name>/items/', methods=['GET', 'POST'])
def showCatalogItems(catalog_name):
    """
    Behavior:
        Query the Catalog and Item tables
        Load public_catalog_entries.html or catalog_entries.html
    Args:
        catalog_name - text string
    Returns:
        body_set - dict, contains the catalog details
        catalog - dict, contains the details of a catalog
        items - dict, contains the items details in a catalog
        items_count - integer, a count of the number of items in a catalog
        Call Flask render_template() function for
        public_catalog_entries.html or catalog_entries.html, passing
        the component body_set, catalog, items and items_count.
    """
    body_set = session.query(Catalog).all()
    catalog = session.query(Catalog).filter_by(Cname=catalog_name).first()
    items = session.query(Item).filter_by(catalog_id=catalog.id).all()
    items_count = session.query(Item).filter_by(catalog_id=catalog.id).count()
    if 'username' not in login_session:
        return render_template(
            'public_catalog_entries.html',
            body_set=body_set, catalog=catalog, items=items,
            items_count=items_count
            )
    else:
        return render_template(
            'catalog_entries.html',
            body_set=body_set,
            catalog=catalog,
            items=items,
            items_count=items_count
            )


@app.route(
    '/catalog/<string:catalog_name>/<string:item_name>/',
    methods=['GET', 'POST']
    )
def showItemDesc(catalog_name, item_name):
    """
    Behavior:
        Query the Item table
        Load public_item_desc.html or item_desc.html
    Args:
        catalog_name, item_name - text string
    Returns:
        item - dict, contains the details of an item
        catalog - dict, contains the details of a catalog
        creator - dict, contains the details of a user
        Call Flask render_template() function for public_item_desc.html
        or item_desc.html, passing the component item, creator and catalog
    """
    item = session.query(Item).filter_by(Iname=item_name).first()
    creator = getUserInfo(item.user_id)
    catalog = session.query(Catalog).filter_by(Cname=catalog_name).first()
    if 'username' not in login_session or creator.id != login_session[
            'user_id']:
        return render_template(
            'public_item_desc.html',
            item=item,
            creator=creator,
            catalog=catalog
            )
    else:
        return render_template(
            'item_desc.html',
            item=item,
            creator=creator,
            catalog=catalog
            )


@app.route('/catalog/<string:item_name>/edit/', methods=['GET', 'POST'])
def editItem(item_name):
    """
    Behavior:
        Query the Item table and edit the item with name item_name
        Load edit_item.html or call the showCatalogItems function
    Args:
        item_name - text string
    Returns:
        editedItem - dict, contains the details of an item
        catalog - dict, contains the details of a catalog
        Call Flask render_template() function for edit_item.html, passing
        the component catalog or call the showCatalogItems function.
        flask flash message.
    """
    editedItem = session.query(Item).filter_by(Iname=item_name).first()
    catalog = session.query(Catalog).filter_by(
        id=editedItem.catalog_id).one_or_none()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.Iname = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['pieces']:
            editedItem.pieces = request.form['pieces']
        if request.form['item_image']:
            editedItem.item_image = request.form['item_image']
        session.add(editedItem)
        session.commit()
        if request.form['name']:
            flash("The item %s has been correctly edited" %
                  request.form['name'])
        else:
            flash("The item %s has been correctly edited" % item_name)
        return redirect(url_for('showCatalogItems',
                                catalog_name=catalog.Cname))
    else:
        return render_template('edit_item.html', item=editedItem)


@app.route('/catalog/<string:catalog_name>/new/', methods=['GET', 'POST'])
def newItem(catalog_name):
    """
    Behavior:
        Create a new item
        Load new_item.html or call the showCatalogItems function
    Args:
        catalog_name - text string
    Returns:
        catalog - dict, contains the details of a catalog
        Call Flask render_template() function for new_item.html or call the
        showCatalogItems function.
        flask flash message
    """
    if request.method == 'POST':
        catalog = session.query(Catalog).filter_by(Cname=catalog_name).first()
        newItem = Item(
            Iname=request.form['name'],
            description=request.form['description'],
            pieces=request.form['pieces'],
            item_image=request.form['item_image'],
            created_at=datetime.now(),
            catalog_id=catalog.id,
            user_id=login_session['user_id']
            )
        session.add(newItem)
        session.commit()
        flash("The item %s has been correctly created" % request.form['name'])
        return redirect(url_for('showCatalogItems', catalog_name=catalog_name))
    else:
        return render_template('new_item.html')


@app.route('/catalog/<string:item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(item_name):
    """
    Behavior:
        Delete the item with name item_name
        Load delete_item.html or call the showCatalogItems function
    Args:
        item_name - text string
    Returns:
        item - dict, contains the details of an item
        catalog - dict, contains the details of a catalog
        Call Flask render_template() function for delete_item.html, passing the
        component item or call the showCatalogItems function.
        flask flash message
    """
    item = session.query(Item).filter_by(Iname=item_name).one_or_none()
    catalog = session.query(Catalog).filter_by(
        id=item.catalog_id).one_or_none()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("The item %s has been correctly deleted" % item_name)
        return redirect(
            url_for(
                'showCatalogItems',
                catalog_name=catalog.Cname)
                )
    else:
        return render_template('delete_item.html', item=item)


@app.route('/catalog/<string:catalog_name>/items/json')
def catalogJson(catalog_name):
    """
    Behavior:
        Provide the details for the items of a catalog on a json format
    Args:
        catalog_name - text string
    Returns:
        items - dict, contains the details of items of a catalog
        catalog - dict, contains the details of a catalog
        text string in a json format
    """
    catalog = session.query(Catalog).filter_by(Cname=catalog_name).first()
    items = session.query(Item).filter_by(catalog_id=catalog.id).all()
    return jsonify(Item=[i.serialize for i in items])


@app.route('/catalog/<string:catalog_name>/<string:item_name>/json')
def itemJson(catalog_name, item_name):
    """
    Behavior:
        Provide the details for an item on a json format
    Args:
        catalog_name - text string
        item_name - text string
    Returns:
        item - dict, contains the details of an item
        text string in a json format
    """
    item = session.query(Item).filter_by(Iname=item_name).first()
    return jsonify(Item=[item.serialize])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
