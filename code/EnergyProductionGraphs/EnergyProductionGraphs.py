import requests
import xml.etree.ElementTree as ET

#Replace with your ENTSO-E API key,
API_KEY = 'YOUR_ENTSOE_API_KEY'

#Example parameters: country code (domain), data type (e.g. 'Actual Total Load'), period,
params = {
    'securityToken': API_KEY,
    'documentType': 'A65',   # Actual Total Load
    'in_Domain': '10YTN-TN------A',   # Tunisia Bidding Zone (if available, else use 10YHU-HU------E for Hungary etc.)
    'periodStart': '202510180000',    # Format YYYYMMDDHH00
    'periodEnd': '202510182300'
}
url = "https://transparency.entsoe.eu/api"

response = requests.get(url, params=params)
xml_data = response.content

#Parse XML response for energy variables,
tree = ET.fromstring(xml_data)
#You may need to navigate through the XML to extract time, value, units, etc.,
for timeseries in tree.findall('.//TimeSeries'):
    prod_type = timeseries.find('.//productionType')
    mRID = timeseries.find(".//mRID")
    for period in timeseries.findall('.//Period'):
        start_time = period.find('.//timeInterval/start').text
        for point in period.findall('.//Point'):
            position = point.find('position').text
            qty = point.find('quantity').text
            print(f"Time: {start_time} | Position: {position} | Quantity: {qty} | Type: {prod_type.text if prod_type is not None else mRID.text}")

#You'll group by productionType (Renewable, Fossil, Hydro, Wind, Solar, Load) as needed