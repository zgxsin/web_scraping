import time
from helper_functions import parse_single_url
from selenium.webdriver import Chrome
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup


class ETHRoomSearch:
    def __init__(self, sv_url="https://studentvillage.ch/en/accommodation/", ls_url="http://reservation.livingscience"
                                                                                    ".ch/en/living"):
        self.sv_url = sv_url
        self.ls_url = ls_url

    def organize_sv_data(self, input_html_segments):
        room_nr = []
        surface_area = []
        orientation = []
        rooms = []
        status = []
        link = []
        # Scrape data for every html segment. This may take some time.
        for html_seg in input_html_segments:
            room_nr.append(html_seg.find("td").a.string)

            surface_area.append(html_seg.find("td", class_="aBDP makelink").string)

            orientation.append(html_seg.find("td", class_="hide_below_768 makelink").string)

            rooms.append(html_seg.find("td", class_="hide_below_1200 makelink").string)

            status.append(html_seg.select("td.makelink")[3].string)

            link.append(html_seg.select("td")[4].get("data-url"))

        scraped_data = pd.DataFrame(
            {'App. Nr': room_nr, 'Surface Area': surface_area, 'Orientation': orientation, "Rooms": rooms,
             "Status": status, "Link": link})
        return scraped_data

    def organize_ls_data(self, input_html_segments):
        app_nr = []
        nr_of_rooms = []
        size = []
        floor = []
        gross_rent = []
        charges = []
        start_of_rent = []
        status = []
        gender = []
        # Scrape data for every html segment: this may take some time.
        for html_seg in input_html_segments:
            app_nr.append(html_seg.find("span", class_="spalte7").text)

            nr_of_rooms.append(html_seg.find("span", class_="spalte4").text)

            size.append(html_seg.find("span", class_="spalte8").text)

            floor.append(html_seg.find("span", class_="spalte1").text)

            gross_rent.append(html_seg.find("span", class_="spalte5").text)

            charges.append(html_seg.find("span", class_="spalte11").text)

            start_of_rent.append(html_seg.find("span", class_="spalte6").text)

            status.append(html_seg.find("span", class_="spalte2").text)

            gender.append(html_seg.find("span", class_="spalte9").text)

        scraped_data = pd.DataFrame(
            {'App. Nr': app_nr, 'Rooms': nr_of_rooms, 'Size': size, "Floor": floor,
             "Gross Rent": gross_rent, "Charges": charges, 'Start of Rent': start_of_rent, 'Status': status,
             'Gender': gender})
        return scraped_data

    def filter_entries_from_sv_url(self):
        soup = parse_single_url(self.sv_url)
        html_segments = soup.find_all("tr", attrs={"data-rel-status": "frei"})
        return html_segments

    def filter_entries_from_ls_url(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # This will not pop up the website window.
        options.add_argument('--headless')
        # You need to install chromedriver by running "sudo apt install chromium-chromedriver",
        # make sure this executable is included in your ${PATH}.
        wb_driver = Chrome(chrome_options=options)

        wb_driver.get(self.ls_url)

        # Check doc here:
        # https://www.selenium.dev/documentation/en/getting_started_with_webdriver/locating_elements/.
        # Selenium-python: https://selenium-python.readthedocs.io/locating-elements.html#locating-elements-by-class-name
        # https://devqa.io/selenium/.
        # Click a button and write text in website: https://pythonspot.com/selenium-click-button/.
        select_element = wb_driver.find_elements_by_css_selector("select#cimmotool_status")
        all_options = select_element[0].find_elements_by_tag_name("option")
        all_options[0].click()
        # Allow some time for the page to load after clicking.
        time.sleep(1)
        page_source = wb_driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        html_segments = soup.findAll("div", class_="row status2")
        return html_segments


if __name__ == "__main__":
    eth_room_search_obj = ETHRoomSearch()
    sv_html_segments = eth_room_search_obj.filter_entries_from_sv_url()
    pandas_data_sv = eth_room_search_obj.organize_sv_data(sv_html_segments)

    ls_html_segments = eth_room_search_obj.filter_entries_from_ls_url()
    pandas_data_ls = eth_room_search_obj.organize_ls_data(ls_html_segments)
    print(pandas_data_sv.to_string() + '\n\n' + pandas_data_ls.to_string())
