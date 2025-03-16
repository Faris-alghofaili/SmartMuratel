from flask import Blueprint,render_template,request,jsonify
from flask_login import login_required,  current_user, LoginManager

views = Blueprint('views',__name__)



views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    print(current_user)  # ✅ This should print the logged-in user
    return render_template('home.html')

    


    
    

