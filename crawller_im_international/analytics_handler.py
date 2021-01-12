from international_handler import InternationalHandler
from datetime import date
from utils import keep_trying, write_csv
import time
from selenium.webdriver.common.action_chains import ActionChains

class AnalyticsHandler(InternationalHandler):

  def __init__(self, browser, origin: str, destination: str, date_going: str, date_back: str, quant_adults: str, agency: str):
    self.browser = browser
    self.origin = origin
    self.destination = destination
    self.date_going = date_going
    self.date_back = date_back
    self.quant_adults = quant_adults
    self.agency = agency
    

  @keep_trying
  def handle(self):
    # self.browser.get(f"https://www.decolar.com/shop/flights/results/roundtrip/{self.origin}/{self.destination}/{self.date_going}/{self.date_back}/{self.quant_adults}/0/0/NA/NA/NA/NA/NA/?from=SB&di=1-0")

    data = []
    # analytics = []

    data.append(self.flight_ticket())

    # for data_des in data:
      # analytics.append(data_des)

    return data

  @keep_trying
  def flight_ticket(self):
    today = date.today().strftime('%Y-%m-%d')
    datas_full = []

    initials_data = ['ANALYTICS', today, self.origin, self.destination, self.date_going, self.date_back, self.agency]
    
    for tickets in range(1, 30):
      values = []

      for data_initials in initials_data:
        values.append(data_initials)

      values.append(self.get_cia_name(tickets, 1))
      values.append(' ')
      values.append(' ')
      values.append(' ')

      for index in range(1, 3):
        for data_ticket in self.get_ticket(tickets, index):
          values.append(data_ticket)

      cost_total = self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{tickets}]/span[1]/cluster/div/div/div[2]/fare/span/span/main-fare/span/span[2]/span/flights-price/span/flights-price-element/span/span/em/span[2]')
      values.append(cost_total.text)

      datas_full.append(values)

    self.browser.close()
    return datas_full

  @keep_trying
  def get_ticket(self, ticket: int, index_data_ticket: int):
    data_ticket = []
    
    if index_data_ticket == 2:
      data_ticket.append(self.get_cia_name(ticket, 2))

    aeroport_going = self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span/cluster/div/div/div[1]/div/span/div/div[2]/span[{index_data_ticket}]/route-choice/div/span[2]/span[1]/route-info-item[1]/span/airport-item/span')
    data_ticket.append(aeroport_going.text)


    actions = ActionChains(self.browser)
    actions.move_to_element(aeroport_going).perform()

    self.browser.execute_script("arguments[0].focus();", aeroport_going)
    
    aeroport_going_time = self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span/cluster/div/div/div[1]/div/span/div/div[2]/span[{index_data_ticket}]/route-choice/ul/li/route/itinerary/div/div/div[2]/itinerary-element[1]/span/span/span')
    data_ticket.append(aeroport_going_time.text)

    aeroport_arrival = self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span/cluster/div/div/div[1]/div/span/div/div[2]/span[{index_data_ticket}]/route-choice/div/span[2]/span[2]/route-info-item[1]/span/airport-item/span')
    data_ticket.append(aeroport_arrival.text)

    aeroport_arrival_time = self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span/cluster/div/div/div[1]/div/span/div/div[2]/span[{index_data_ticket}]/route-choice/ul/li/route/itinerary/div/div/div[3]/itinerary-element[1]/span/span/span/span[1]')
    data_ticket.append(aeroport_arrival_time.text)

    aeroport_arrival_time_day = self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span/cluster/div/div/div[1]/div/span/div/div[2]/span[{index_data_ticket}]/route-choice/ul/li/route/itinerary/div/div/div[3]/itinerary-element[1]/span/span/span/span[2]')
    data_ticket.append(aeroport_arrival_time_day.text)
    
    flighting_duration = self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span/cluster/div/div/div[1]/div/span/div/div[2]/span[{index_data_ticket}]/route-choice/ul/li/route/itinerary/div/div/div[3]/itinerary-element[2]/span/duration-item/span/span')
    data_ticket.append(flighting_duration.text)

    type_of_percurse = self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span/cluster/div/div/div[1]/div/span/div/div[2]/span[{index_data_ticket}]/route-choice/ul/li/route/itinerary/div/div/div[2]/itinerary-element[2]/span/stops-count-item/span/span/span[1]')
    data_ticket.append(type_of_percurse.text)

    for list_bag in range(1, 4):
      backpack = self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span/cluster/div/div/div[1]/div/span/div/div[2]/span[{index_data_ticket}]/route-choice/ul/li/route/itinerary/div/div/div[4]/itinerary-element[1]/span/baggage-item/span/span/span[{list_bag}]/i')
      if 'NOT_INCLUDED' in backpack.get_attribute("class").upper():
        data_ticket.append('0')
      else:
        data_ticket.append('1')

    return data_ticket

  @keep_trying
  def get_cia_name(self, ticket: int, index: int) -> str:
    try:
      return self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span/cluster/div/div/div[1]/div/span/div/div[2]/span[{index}]/route-choice/ul/li/route/itinerary/div/div/div[1]/itinerary-element[2]/span/itinerary-element-airline/span/span/span/span/span[2]/span').text.upper()
    except Exception as e:
      try:
        return self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span[1]/cluster/div/div/div[1]/div/span/div/div[2]/span[{index}]/route-choice/ul/li/route/itinerary/div/div/div[1]/itinerary-element[2]/span/itinerary-element-airline/span[1]/span/span/span[2]/span/airline-logo/img').get_attribute('alt').upper()
      except Exception as e:
        return self.browser.find_element_by_xpath(f'//*[@id="clusters"]/span[{ticket}]/span/cluster/div/div/div[1]/div/span/div/div[2]/span[{index}]/route-choice/ul/li/route/itinerary/div/div/div[1]/itinerary-element[2]/span/itinerary-element-airline/span[1]/span/span/span[2]/span/airline-logo/img').get_attribute('alt').upper()