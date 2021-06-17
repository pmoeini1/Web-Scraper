from urllib.request import urlopen
import csv

# access webpage
url = "https://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption"
page = urlopen(url)
# read html
html_bytes = page.read()
html = html_bytes.decode("utf-8")
# isolate table body
table = html[html.find("<tbody>") + len("<tbody"):html.find("</tbody>")]
# split into rows
rows = table.split("<tr>")
# remove 1st row and 2nd row
rows.pop(0)
rows.pop(0)

# write info to .csv file
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Rank", "Country", "Total Consumption (GWh/yr)"])
    # access country name and energy consumption
    count = 1
    for row in rows:
        # split table columns into elements
        items = row.split("<td>")
        # isolate country name in its element
        countryItem = items[2]
        countryItemTags = countryItem.split(">")
        countryTag = countryItemTags[len(countryItemTags) - 3]
        country = countryTag[:countryTag.find("</a")]
        # isolate consumption in its element
        consumptionItem = items[3]
        consumption = consumptionItem[:consumptionItem.find("</td>")]
        # remove columns (to allow conversion to float)
        consumptionClean = consumption.split(",")
        consumption = "".join(consumptionClean)
        # write to .csv file if country variable is not empty or whitespace
        if (country and country.strip()):
            writer.writerow([count, country, consumption])
            count+=1