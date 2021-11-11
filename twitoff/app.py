from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user, get_all_usernames
from .predict import predict_user

def create_app():
    
    # initialize our app
    app = Flask(__name__)

    #Database configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Give app access to DB
    DB.init_app(app)

    # Listen to the "route"
    @app.route('/')
    def root():
        # query the DB for all Users
        return render_template('base.html', title="Home", users= User.query.all())
    
    
    @app.route('/update')
    def update():
        '''update all users'''
        usernames = get_all_usernames()
        for username in usernames:
            add_or_update_user(username)
        return "All Users Have Been Updated"


    #title of site for now

    @app.route('/reset')
    def reset():
        # Remove everything from the database
        DB.drop_all()
        # Create database file initially
        DB.create_all()
        return render_template('base.html', title='Reset Database')
    
    # API ENDPOINTS (Querying and manipulating data in a database)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])

    def user(name=None, message=''):
        # request.values is pulling data from html
        # use the username from the URL (route)
        # or grab it from the dropdown menu
        name = name or request.values['user_name']

        # If the user exists in the DB update it, and query for it
        # If the user does not exist 
        
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f"User {name} Successfully Added!"

            #From the user that was just added / Updated 
            # get their tweets to display on the /user/<name> page
            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = f"Error adding {name}: {e}"

            tweets = []

        return render_template('user.html', title=name, tweets=tweets, message=message)


    @app.route('/compare', methods=['POST'])
    def compare():
        user0 , user1 = sorted([request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            if prediction == 0:
                predicted_user = user0
                non_predicted_user = user1
            else:
                predicted_user = user1
                non_predicted_user = user0
            message = f"'{request.values['tweet_text']}' is more likely to be said by '{predicted_user}' than by '{non_predicted_user}'"

        return render_template('prediction.html', title='Prediction', message=message)
        
    return app