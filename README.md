Prerequisites
•	Python 3.x
•	Google Chrome browser
•	ChromeDriver (compatible with the installed Chrome version)
•	Selenium Python package
________________________________________
Instructions to Run
1.	Install selenium  :   !pip install selenium
2.	Download ChromeDriver  : From Web
3.	Ensure you have Chrome on your PC
________________________________________
Configuration
1.	Update the following variables in the script:
o	Chromedriver_location: Update the chromedriver location
o	username: Your Amazon account email.
o	password: Your Amazon account password.
o	categories: List of categories to scrape.
________________________________________
Usage
1.	Run the script:   python -u "location of python file "
2.	The script will:
o	Log into Amazon.
o	Navigate through each category.
o	Scroll to load items.
o	Extract product information.
o	Save the data into data.json.
________________________________________
Output: The output is a JSON file named data.json, containing a list of dictionaries where each dictionary represents a product. The script handles missing elements gracefully using default values.________________________________________
