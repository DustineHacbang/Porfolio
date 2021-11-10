# Import Flask to allow us to create our app
from flask_app import app  
from flask_app.controllers import users, sightings

# Ensure this file is being run directly and not from a different module    
if __name__=="__main__":  
# Run the app in debug mode.     
    app.run(debug=True)   