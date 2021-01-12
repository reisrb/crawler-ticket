from utils import keep_trying, write_csv
from international_handler import InternationalHandler
import time
from datetime import date

class ResumeHandler(InternationalHandler):
  def __init__(self, browser, origin: str, destination: str, date_going: str, date_back: str, quant_adults: str, agency: str):
    self.browser = browser
    self.origin = origin
    self.destination = destination
    self.date_going = date_going
    self.date_back = date_back
    self.quant_adults = quant_adults
    self.agency = agency
    

  @keep_trying
  def get_agency_name(self, column: int) -> str:
    company = self.browser.find_element_by_xpath(f'/html/body/div[12]/div/div/div/div[2]/div/div[2]/div/span[11]/toolbox-tabs/div/tabs/div/div[2]/tab[1]/div/airlines-matrix/span[1]/div/div/div/div/airlines-matrix-airline[{column}]/ul/li[1]/div/div/div[2]')
    return company.text

  @keep_trying
  def get_element(self, row: int, column: int) -> str:
    valores = self.browser.find_element_by_xpath(f'/html/body/div[12]/div/div/div/div[2]/div/div[2]/div/span[11]/toolbox-tabs/div/tabs/div/div[2]/tab[1]/div/airlines-matrix/span[1]/div/div/div/div/airlines-matrix-airline[{column}]/ul/li[{row}]/span/flights-price/span/flights-price-element/span/span/em/span[2]')
    return valores.text

  def columnList(self, column: int):
    today = date.today().strftime('%Y-%m-%d')
    data = []
    row = []

    initials_data = ['RESUMO', today, self.origin, self.destination, self.date_going, self.date_back, self.agency, self.get_agency_name(column)]
    for dado in initials_data:
      row.append(dado)
      
    for dado in range(2, 5):
      row.append(self.get_element(dado, column))
    data.append(row)

    return data

  @keep_trying
  def handle(self):
    data = []
    self.browser.get(f"https://www.decolar.com/shop/flights/results/roundtrip/{self.origin}/{self.destination}/{self.date_going}/{self.date_back}/{self.quant_adults}/0/0/NA/NA/NA/NA/NA/?from=SB&di=1-0")
    time.sleep(15)
    self.clicked_right = False
    while True:
      if self.clicked_right:
        for index in self.columnList(4):
          data.append(index)
      else:
        for count in range(1,5):
          for index in self.columnList(count):
            data.append(index)

      try:
        self.browser.find_element_by_class_name('airline-matrix-right').click()
        self.clicked_right = True
          
        continue
      except Exception as e:
        print(e)
      break
        
    return data