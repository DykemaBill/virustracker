from flask import Flask, render_template, json, request
import requests, logging, time

# Setup logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='virustracker.log')

# Configuration file name
config_file = 'config'
logging.info('Reading config file ' + config_file + '.json')

# Configuration variables
virustracker_logo = ""
virustracker_email = ""
virustracker_apiroot = ""

# Read configuration file
config_error = False
dataread_records = []
def config_file_read():
    dataread_records.clear()
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
    except IOError:
        print('Problem opening ' + config_file + '.json, check to make sure your configuration file is not missing.')
        logging.info('Problem opening ' + config_file + '.json, check to make sure your configuration file is not missing.')
        global config_error
        config_error = True

config_file_read()

# Get updated data for US and Canada in North America
pulldatetime = time.strftime("%Y-%m-%d_%H%M%S")
data_us = requests.get(virustracker_apiroot + "/countries/USA")
if data_us.status_code == 200:
    print("Got USA data: " + data_us.text)
    data_us_confirmed = data_us['confirmed'][0]['value'] # Need to fix this
    print("US confirmed is: " + data_us_confirmed)
else:
    print("No USA data: " + data_us.text)

# Create Flask app to build site
app = Flask(__name__)

# Root page
@app.route('/')
def root():
    logging.info(request.remote_addr + ' ==> Root page ')
    return render_template('na.html', logo=virustracker_logo, apiroot=virustracker_apiroot, email=virustracker_email)

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