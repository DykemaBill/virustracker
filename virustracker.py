from flask import Flask, render_template, json, request, redirect, url_for
import requests, logging, logging.handlers, time, numbers, os, platform, sys

# Configuration file name
config_file = 'virustracker'

# Set default configuration variables
virustracker_email = "needtosetinconfig@nowhere.com"
virustracker_logo = "needtosetinconfig"
virustracker_logosize = [ 100, 100 ] # This is width and height
virustracker_logfilesize = [ 10000, 9 ] # 10000 is 10k, 9 is 10 total copies
virustracker_pagerefresh = 3600 # This is in seconds
virustracker_apiroot = "https://needtosetinconfig/api"

# Function to read configuration file
config_error = False
countries_config = []
regions_config = []
def config_file_read():
    global countries_config
    countries_config.clear()
    global regions_config
    regions_config.clear()
    try:
        with open(config_file + '.cfg', 'r') as json_file:
            json_data = json.loads(json_file.read())
            global virustracker_email
            global virustracker_logo
            global virustracker_logosize
            global virustracker_logfilesize
            global virustracker_pagerefresh
            global virustracker_apiroot
            virustracker_logfilesize.clear()
            virustracker_logfilesize.append(json_data['logfilesize'][0])
            virustracker_logfilesize.append(json_data['logfilesize'][1])
            virustracker_pagerefresh = json_data['pagerefresh']
            virustracker_email = json_data['email']
            virustracker_logo = json_data['logo']
            virustracker_logosize.clear()
            virustracker_logosize.append(json_data['logosize'][0])
            virustracker_logosize.append(json_data['logosize'][1])
            virustracker_apiroot = json_data['apiroot']
            for country in json_data['countries']:
                countries_config.append(country['iso3'])
            for region in json_data['countries']:
                regions_config.append(region['regions'])
    except IOError:
        print('Problem opening ' + config_file + '.cfg, check to make sure your configuration file is not missing.')
        global config_error
        config_error = True

# Read configuration file
config_file_read()

# Set log name
log_file = 'virustracker.log'
# Start logger with desired output level
logger = logging.getLogger('Logger')
logger.setLevel(logging.INFO)
# Setup log handler to manage size and total copies
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=virustracker_logfilesize[0], backupCount=virustracker_logfilesize[1])
# Setup formatter to prefix each entry with date/time 
formatter = logging.Formatter("%(asctime)s - %(message)s")
# Add formatter
handler.setFormatter(formatter)
# Add handler
logger.addHandler(handler)

# Starting up
logger.info('****====****====****====****====****==== Starting up ====****====****====****====****====****')

# Config file status
if config_error == True:
    print ("Unable to read config")
    logger.info('Problem opening ' + config_file + '.cfg, check to make sure your configuration file is not missing.')
else:
    print ("Configuration file read")
    logger.info('Log file size is set to ' + str(virustracker_logfilesize[0]) + ' bytes and ' + str(virustracker_logfilesize[1]) + ' copies')
    logger.info('Email is set to: ' + virustracker_email)
    logger.info('Logo is set to: ' + virustracker_logo)
    logger.info('Logo size is set to: ' + str(virustracker_logosize[0]) + ', ' + str(virustracker_logosize[1]))
    logger.info('Page refresh is set to: ' + str(virustracker_pagerefresh))
    logger.info('API path root is set to: ' + virustracker_apiroot)
    logger.info('Countries to display: ' + str(countries_config))
    logger.info('Regions to display: ' + str(regions_config))

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
        logger.info(virusdata_world_updated + ' ==> World confirmed: ' + str(virusdata_world_confirmed_new) + ', recovered: ' + str(virusdata_world_recovered_new) + ', deaths: ' + str(virusdata_world_deaths_new))
    else:
        print("No world data: " + virusdata_world.text)
        logger.info('World  ==> failed to get data')

# Pull data
if config_error == False:
    data_world_pull()

# Class to collect array and then pass to HTML page
class CountryJSONtoArray:
    def __init__(self, confirmed, recovered, deaths, lastUpdate):
        self.virusdata_confirmed = confirmed
        self.virusdata_recovered = recovered
        self.virusdata_deaths = deaths
        self.virusdata_updated = lastUpdate

# Data variables
if config_error == False:
    countries_data = []

# Function to pull countries data
def data_countries_pull():
    # Get updated data for countries
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
            logger.info(virusdata_country_updated + ' ==> ' + country + ' confirmed: ' + str(virusdata_country_confirmed) + ', recovered: ' + str(virusdata_country_recovered) + ', deaths: ' + str(virusdata_country_deaths))
            countries_data.append(CountryJSONtoArray(**virusdata_country_json)) # Using this to make it easier to use with Jinja
        else:
            print("No " + country + " data: " + virusdata_country.text)
            logger.info(country + '  ==> failed to get data')

# Pull country data
if config_error == False:
    data_countries_pull()

# Class to collect array and then pass to HTML page
class RegionJSONtoArray:
    def __init__(self, region_short, provinceState, countryRegion, lastUpdate, lat, long, confirmed, recovered, deaths, active, admin2, fips, combinedKey, incidentRate, peopleTested, peopleHospitalized, uid, iso2, iso3):
        self.virusdata_region_short = region_short
        self.virusdata_country = iso3
        self.virusdata_region = combinedKey
        self.virusdata_confirmed = confirmed
        self.virusdata_recovered = recovered
        self.virusdata_deaths = deaths
        self.virusdata_updated = lastUpdate

# Class to create non-duplicate list of short region names for filter controls
class RegionShortJSONtoArray:
    def __init__(self, iso3, region_short):
        self.virusdata_country = iso3
        self.virusdata_region_short = region_short

# Data variables
if config_error == False:
    regions_data = []

# Region short list variables
if config_error == False:
    regions_short_list = []

# Function to pull regions data
def data_regions_pull():
    # Get updated data for countries
    global regions_data
    global regions_short_list
    region_previous = ""
    regions_data.clear()
    regions_short_list.clear()

    # Get confirmed data for all regions
    virusdata_regions = requests.get(virustracker_apiroot + "/confirmed")
    if virusdata_regions.status_code == 200:
        virusdata_regions_json = virusdata_regions.json()
        for country_regions in regions_config:
            # Iterate through each region from the country region list
            for region in country_regions:
            
                # Assume current region will not be found
                region_found = False

                for country_regions_item in virusdata_regions_json:

                    # Look for region and get values for it
                    if country_regions_item['combinedKey'] == region:

                        # Found data for current region
                        region_found = True

                        # Parse out just region/province/state name
                        virusdata_region_list = region.split(',') # Split into parts
                        virusdata_region_list_length = len(virusdata_region_list) # Number of parts
                        virusdata_region_short_space = virusdata_region_list[virusdata_region_list_length-2] # Get the second to last part
                        virusdata_region_short = virusdata_region_short_space.lstrip() # Remove leading space
                        print(region + " short name is: " + str(virusdata_region_short))

                        # Get new confirmed value
                        virusdata_region_confirmed = int(country_regions_item['confirmed'])
                        print(region + " confirmed is: " + str(virusdata_region_confirmed))

                        # Get new recovered value
                        #virusdata_region_recovered = int(country_regions_item['recovered'])
                        #print(region + " recovered is: " + str(virusdata_region_recovered))

                        # Get new deaths value
                        virusdata_region_deaths = int(country_regions_item['deaths'])
                        print(region + " deaths is: " + str(virusdata_region_deaths))

                        # Get latitude and longitude
                        virusdata_region_gis = []
                        virusdata_region_gis.append(float(country_regions_item['lat']))
                        virusdata_region_gis.append(float(country_regions_item['long']))
                        print(region + " GIS point is: " + str(virusdata_region_gis))

                        # Get new last updated value
                        virusdata_region_updated = int(country_regions_item['lastUpdate'])
                        print(region + " updated: " + str(virusdata_region_updated))

                        # Log new values
                        #logger.info(str(virusdata_region_updated) + ' ==> ' + region + ' confirmed: ' + str(virusdata_region_confirmed) + ', recovered: ' + str(virusdata_region_recovered) + ', deaths: ' + str(virusdata_region_deaths))
                        logger.info(str(virusdata_region_updated) + ' ==> ' + region + ' confirmed: ' + str(virusdata_region_confirmed) + ', deaths: ' + str(virusdata_region_deaths))
                        regions_data.append(RegionJSONtoArray(virusdata_region_short, **country_regions_item)) # Using this to make it easier to use with Jinja

                        if virusdata_region_short != region_previous:
                            regions_short_list.append(RegionShortJSONtoArray(country_regions_item['iso3'], virusdata_region_short)) # Using this to make it easier to use with Jinja also
                            region_previous = virusdata_region_short

                if region_found == False:
                    print("No region data for: " + region)
                    logger.info(region + ' no data')
    else:
        print("No regions data: " + virusdata_regions.text)
        logger.info('Regions  ==> failed to get data')

# Pull country data
if config_error == False:
    data_regions_pull()

# Create Flask app to build site
app = Flask(__name__)

# Root page
@app.route('/')
def root():
    if config_error == False:
        logger.info(request.remote_addr + ' ==> Root page ')
        data_world_pull()
        data_countries_pull()
        data_regions_pull()
        return render_template('main.html', logo=virustracker_logo, logosize=virustracker_logosize, pagerefresh=virustracker_pagerefresh, apiroot=virustracker_apiroot, email=virustracker_email, virusdata_world_confirmed=virusdata_world_confirmed, virusdata_world_confirmed_updated=virusdata_world_confirmed_updated,virusdata_world_recovered=virusdata_world_recovered, virusdata_world_recovered_updated=virusdata_world_recovered_updated, virusdata_world_deaths=virusdata_world_deaths, virusdata_world_deaths_updated=virusdata_world_deaths_updated, virusdata_world_updated=virusdata_world_updated, country_names=countries_config, countries_data=countries_data, regions_short_list=regions_short_list, regions_data=regions_data)
    else:
        return redirect(url_for('errorpage'))

# About page
@app.route('/about')
def about():
    logger.info(request.remote_addr + ' ==> About page ')
    return render_template('about.html', logo=virustracker_logo, logosize=virustracker_logosize, apiroot=virustracker_apiroot, email=virustracker_email)

# Maintenance page
@app.route('/maint')
def maint():
    logger.info(request.remote_addr + ' ==> Maintenance page ')
    return render_template('maintenance.html', logo=virustracker_logo, logosize=virustracker_logosize, email=virustracker_email)

# Error page
@app.route('/errorpage')
def errorpage():
    logger.info(request.remote_addr + ' ==> Error page ')
    return render_template('error.html')

# IE notice page
@app.route('/ienotice')
def ienotice():
    logger.info(request.remote_addr + ' ==> IE notice page ')
    return render_template('ienotice.html')

# Status page
@app.route('/status')
def status():
    logger.info(request.remote_addr + ' ==> Status page ')
    running_python = sys.version.split('\n')
    running_host = platform.node()
    running_os = platform.system()
    running_hardware = platform.machine()
    try:
        with open(config_file + '.cfg', 'r') as text_file:
            config_data = text_file.read()
    except IOError:
        print('Problem opening ' + config_file + '.cfg, check to make sure your configuration file is not missing.')
        config_data = "Unable to read config file " + config_file + '.cfg'
    try:
        with open(log_file, 'r') as logging_file:
            log_data = logging_file.read()
    except IOError:
        print('Problem opening ' + log_file + ', check to make sure your log file location is valid.')
        log_data = "Unable to read log file " + log_file
    return render_template('status.html', running_python=running_python, running_host=running_host, running_os=running_os, running_hardware=running_hardware, config_data=config_data, log_data=log_data)

# Run in debug mode if started from CLI
if __name__ == '__main__':
    app.run(debug=True)