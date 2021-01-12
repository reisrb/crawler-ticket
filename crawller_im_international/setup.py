from utils import write_csv
from analytics_handler import AnalyticsHandler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from resume_handler import ResumeHandler

if __name__ == '__main__':
  data = []
  #options = webdriver.ChromeOptions()
  #options.add_argument("headless")
  #browser = webdriver.Chrome(chrome_options=options)
  browser = webdriver.Chrome()
  resume_handler = ResumeHandler(browser, 'GRU', 'VDC', '2020-12-27', '2021-01-19', '2', 'DECOLAR')
  data.append(resume_handler.handle())
  analytics_handler = AnalyticsHandler(browser, 'GRU', 'VDC',  '2020-12-27', '2021-01-19', '2', 'DECOLAR')
  for ronaldo in analytics_handler.handle():
    data.append(ronaldo)

  write_csv(data)
