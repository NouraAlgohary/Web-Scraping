from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# A WebDriver instance
driver = webdriver.Chrome()

# Website url
url = "http://books.toscrape.com/"
driver.get(url)

books_list = []

#Class name for the class that contains all book information
class_name = '.col-xs-6, .col-sm-4, .col-md-3, .col-lg-3'num_pages = 50

# Locator for the next page button
next_page_button_locator = (By.XPATH, '//li[@class="next"]/a')

for page_number in range(num_pages):
    print(f"Scraping page {page_number + 1}")

    if page_number != 0:
        try:
            # Explicitly wait for the next page button to be present
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(next_page_button_locator))

            # Explicitly wait for the next page button to be clickable
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(next_page_button_locator))

            # Find the next page button and click it
            next_page_button = driver.find_element(*next_page_button_locator)
            next_page_button.click()


        except Exception as e:
            print(f"Exception: {type(e).__name__} - {e}. Refreshing the page and retrying click.")
            driver.refresh()


    # Get the updated list of books after navigating to the next page
    books = driver.find_elements(By.CSS_SELECTOR, class_name)

    for book in books:
        stars = book.find_element(By.CSS_SELECTOR, '.star-rating').get_attribute('class')
        title = book.find_element(By.CSS_SELECTOR, 'h3 a').get_attribute('title')
        price = book.find_element(By.CSS_SELECTOR, '.price_color').text
        availability = book.find_element(By.CSS_SELECTOR, '.instock.availability').text

        book_item = {
            "stars": stars,
            "title": title,
            "price": price,
            "availability":availability
        }
        books_list.append(book_item)

df = pd.DataFrame(books_list)

# Save the dataframe to a CSV file
df.to_csv('path-to-folder/booksToScrape.csv', index=True)

# Close the browser
driver.quit()
