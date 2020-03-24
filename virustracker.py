from flask import Flask, render_template, json, request
import requests, logging, time, os

# Setup logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='virustracker.log')

# Starting up
logging.info('****====****====****====****====****==== Starting up ====****====****====****====****====****')

# Configuration file name
config_file = 'config'
logging.info('Reading config file ' + config_file + '.json')

# Read configuration variables
virustracker_logo = ""
virustracker_email = ""
virustracker_apiroot = ""

# Function to read configuration file
config_error = False
countries_config = []
def config_file_read():
    global countries_config
    countries_config.clear()
    try:
        with open(config_file + '.json', 'r') as json_file:
            json_data = json.loads(json_file.read())
            global virustracker_logo
            global virustracker_email
            global virustracker_apiroot
            virustracker_logo = json_data['logo']
            logging.info('Logo is set to: ' + virustracker_logo)
            virustracker_apiroot = json_data['apiroot']
            logging.info('API path root is set to: ' + virustracker_apiroot)
            virustracker_email = json_data['email']
            logging.info('Email is set to: ' + virustracker_email)
            for country in json_data['countries']:
                countries_config.append(country)
            logging.info('Countries to display: ' + str(countries_config))
    except IOError:
        print('Problem opening ' + config_file + '.json, check to make sure your configuration file is not missing.')
        logging.info('Problem opening ' + config_file + '.json, check to make sure your configuration file is not missing.')
        global config_error
        config_error = True

# Read configuration file
config_file_read()

# Data variables
virusdata_world_confirmed = 0
virusdata_world_confirmed_updated = False
virusdata_world_recovered = 0
virusdata_world_recovered_updated = False
virusdata_world_deaths = 0
virusdata_world_deaths_updated = False
virusdata_world_updated = ""

# Function to pull data
def data_world_pull():
    # Get updated data for entire world
    pulldatetime = time.strftime("%Y-%m-%d_%H%M%S")
    virusdata_world = requests.get(virustracker_apiroot)
    if virusdata_world.status_code == 200:
        print("Got entire world data: " + virusdata_world.text)
        virusdata_world_json = virusdata_world.json()
        global virusdata_world_confirmed
        global virusdata_world_confirmed_updated
        global virusdata_world_recovered
        global virusdata_world_recovered_updated
        global virusdata_world_deaths
        global virusdata_world_deaths_updated
        global virusdata_world_updated

        # Get new confirmed value
        virusdata_world_confirmed_new = int(virusdata_world_json['confirmed']['value'])
        # Check to see if new value is greater
        if virusdata_world_confirmed_new < virusdata_world_confirmed:
            # Since it is not greater, it could be bad data
            virusdata_world_confirmed_updated = False
        else:
            # Since it is greater, use it
            virusdata_world_confirmed = virusdata_world_confirmed_new
            virusdata_world_confirmed_updated = True
        print("World confirmed is: " + str(virusdata_world_confirmed))

        # Get new recovered value
        virusdata_world_recovered_new = int(virusdata_world_json['recovered']['value'])
        # Check to see if new value is greater
        if virusdata_world_recovered_new < virusdata_world_recovered:
            # Since it is not greater, it could be bad data
            virusdata_world_recovered_updated = False
        else:
            # Since it is greater, use it
            virusdata_world_recovered = virusdata_world_recovered_new
            virusdata_world_recovered_updated = True
        print("World recovered is: " + str(virusdata_world_recovered))

        # Get new deaths value
        virusdata_world_deaths_new = int(virusdata_world_json['deaths']['value'])
        # Check to see if new value is greater
        if virusdata_world_deaths_new < virusdata_world_deaths:
            # Since it is not greater, it could be bad data
            virusdata_world_deaths_updated = False
        else:
            # Since it is greater, use it
            virusdata_world_deaths = virusdata_world_deaths_new
            virusdata_world_deaths_updated = True
        print("World deaths is: " + str(virusdata_world_deaths))

        # Get new last updated value
        virusdata_world_updated = virusdata_world_json['lastUpdate']
        print("Updated: " + virusdata_world_updated)

        # Log new values
        logging.info(virusdata_world_updated + ' ==> World confirmed: ' + str(virusdata_world_confirmed_new) + ', recovered: ' + str(virusdata_world_recovered_new) + ', deaths: ' + str(virusdata_world_deaths_new))
    else:
        print("No world data: " + virusdata_world.text)
        logging.info('World  ==> failed to get data')

# Pull data
data_world_pull()

# Class to collect array and then pass to HTML page
class JSONtoArray:
    def __init__(self, confirmed, recovered, deaths, lastUpdate):
        self.virusdata_confirmed = confirmed
        self.virusdata_recovered = recovered
        self.virusdata_deaths = deaths
        self.virusdata_updated = lastUpdate

# Data variables
countries_data = []

# Function to pull countries data
def data_countries_pull():
    # Get updated data for countries
    pulldatetime = time.strftime("%Y-%m-%d_%H%M%S")
    global countries_data
    countries_data.clear()
    for country in countries_config:
        virusdata_country = requests.get(virustracker_apiroot + "/countries/" + country)
        if virusdata_country.status_code == 200:
            print("Got " + country + " data: " + virusdata_country.text)
            virusdata_country_json = virusdata_country.json()

            # Get new confirmed value
            virusdata_country_confirmed = int(virusdata_country_json['confirmed']['value'])
            print(country + " confirmed is: " + str(virusdata_country_confirmed))

            # Get new recovered value
            virusdata_country_recovered = int(virusdata_country_json['recovered']['value'])
            print(country + " recovered is: " + str(virusdata_country_recovered))

            # Get new deaths value
            virusdata_country_deaths = int(virusdata_country_json['deaths']['value'])
            print(country + " deaths is: " + str(virusdata_country_deaths))

            # Get new last updated value
            virusdata_country_updated = virusdata_country_json['lastUpdate']
            print(country + " updated: " + virusdata_country_updated)

            # Log new values
            logging.info(virusdata_country_updated + ' ==> ' + country + ' confirmed: ' + str(virusdata_country_confirmed) + ', recovered: ' + str(virusdata_country_recovered) + ', deaths: ' + str(virusdata_country_deaths))
            countries_data.append(JSONtoArray(**virusdata_country_json)) # Using this to make it easier to use with Jinja
        else:
            print("No " + country + " data: " + virusdata_country.text)
            logging.info(country + '  ==> failed to get data')

# Pull country data
data_countries_pull()

# Create Flask app to build site
app = Flask(__name__)

# Root page
@app.route('/')
def root():
    logging.info(request.remote_addr + ' ==> Root page ')
    data_world_pull()
    data_countries_pull()
    return render_template('main.html', logo=virustracker_logo, apiroot=virustracker_apiroot, email=virustracker_email, virusdata_world_confirmed=virusdata_world_confirmed, virusdata_world_confirmed_updated=virusdata_world_confirmed_updated,virusdata_world_recovered=virusdata_world_recovered, virusdata_world_recovered_updated=virusdata_world_recovered_updated, virusdata_world_deaths=virusdata_world_deaths, virusdata_world_deaths_updated=virusdata_world_deaths_updated, virusdata_world_updated=virusdata_world_updated, country_names=countries_config, countries_data=countries_data)

# About page
@app.route('/about')
def about():
    logging.info(request.remote_addr + ' ==> About page ')
    return render_template('about.html', logo=virustracker_logo, apiroot=virustracker_apiroot, email=virustracker_email)

# Maintenance template page
@app.route('/maint')
def maint():
    logging.info(request.remote_addr + ' ==> Maintenance page ')
    return render_template('maintenance.html', logo=virustracker_logo, email=virustracker_email)

# Run in debug mode if started from CLI
if __name__ == '__main__':
    app.run(debug=True)