import time
import argparse
import requests
from bs4 import BeautifulSoup as bs

def get_web_driver():
	from selenium import webdriver
	from selenium.webdriver.chrome.service import Service
	from selenium.webdriver.chrome.options import Options
	from webdriver_manager.chrome import ChromeDriverManager

	chrome_options = Options()
	chrome_options.headless = True
	chrome_service = Service(ChromeDriverManager().install())

	driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
	return driver
	

def get_links(url):
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC

	# Get web driver using Selenium
	print('Loading web driver...')
	print('If this takes a long time (>10s), restart the program.')
	print('It occurs because the socket is wating to be ready.')
	driver = get_web_driver()
	print('Driver is ready.')
	driver.implicitly_wait(3)
	driver.get(url)

	# Wait until the data list is loaded
	element = WebDriverWait(driver, 5) \
				.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-busy]')))

	# Scroll to bottom once (to load more data)
	# If scrolling once is not enough, repeat these script as many times as you want.
	driver.execute_script('elem = document.getElementsByTagName("body")[0];')
	driver.execute_script('elem = elem.firstChild.firstChild.firstChild;')
	driver.execute_script('elem.scrollTo(0, elem.scrollHeight)')
	time.sleep(2) # wait for loading the data

	html = driver.page_source
	soup = bs(html, 'html.parser')
	driver.quit()

	page_links = []
	data_links = soup.select('div[aria-busy] > div')
	for link in data_links:
		soup = bs(str(link), 'html.parser')
		tag = soup.select('a')
		page_links.append(tag[0]['href'])

	print('')
	print(len(data_links), ' data are detected')
	print('If you think there are more data, please read line 37~38 of code.')


	# Open the data page and get the data
	down_links = []
	down_names = []

	for i, link in enumerate(page_links):
		print(i + 1, ' data link is checking... : ', end='')
		html = requests.get(link)
		soup = bs(html.text, 'html.parser')
		
		# Read filename
		names = soup.select('div:has(button[tooltip="File info"]) > div:nth-child(1) > span')
		down_names.append(''.join([names[0].text, names[1].text]))
		print(down_names[i])
		
		# Save download link
		tag = soup.select('main > div > div:nth-last-child(2) a')
		down_links.append(tag[0]['href'])

	return down_names, down_links

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Springer nature figshare collection downloader')
	parser.add_argument('URL', type=str, help='Target url')
	parser.add_argument('--out_names', type=str, default='names.txt', help='List of data names')
	parser.add_argument('--out_links', type=str, default='links.txt', help='List of data links')
	args = parser.parse_args()

	names, links = get_links(args.URL)
	with open(args.out_names, 'w') as f:
		f.writelines('\n'.join(names))
	with open(args.out_links, 'w') as f:
		f.writelines('\n'.join(links))

	print('Done')
