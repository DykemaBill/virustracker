# virustracker

Python Flask application that displays virus information in a customizable format

# Description

Web application written in Python using Flask which provides a single root page to display current World and customizable country COVID-19 information.  This application reads from a configuration file which can be used to customize the following:

- Support email address for your page
- Page logo (set to [World Health Organization](http://who.int)'s logo by default)
- API root (set to [Muhammad Mustadi](https://mathdro.id)'s [COVID-19 JSON API](https://github.com/mathdroid/covid-19-api) by default)
- Countries, can be used to set the countries you would like to see information on

# To-Do's for the author

- Add desired locations to configuration file rather than hardcoding - DONE
- Change code to loop through locations from configuration file - DONE
- Update HTML page to receive array of locations - DONE
- Clean-up HTML page look and feel - DONE
- Add additional links to external charts/graphs, possibly embed them - DONE
- Page auto refresh (not frequent) for those that might leave it open or use it in a kiosk - DONE
- On data pull error, add message rather than just displaying a 0 - DONE
- Add favicon - DONE
- Reduce KPI size for smaller displays - DONE
- Rename configuration file to match application name - DONE
- Add logo size to configuration file - DONE
- Move world and country titles to the lefthand area to make more room to add cities/provinces - DONE
- Add cities/provinces to configuration file and display under countries - DONE
- Change regions to hide by default in the page - DONE
- License notice added - DONE
- Log clean-up/archive - DONE
- Add page refresh time to configuration - DONE
- Add country maps and remove embedded world map
- Add filter by state option
- Look into direct OData access to Johns Hopkins University, likely separate project

# License

[MIT License 2020](https://mit-license.org), [Bill Dykema](https://github.com/DykemaBill).

This Python Flask application uses [Muhammad Mustadi](https://mathdro.id)'s [COVID-19 JSON API](https://github.com/mathdroid/covid-19-api) to get data.
Data comes from the [Johns Hopkins University](https://www.jhu.edu), it may not be used for commercial purposes.

![virustracker_screenshot](https://github.com/DykemaBill/virustracker/blob/master/virustrackerSS.png)