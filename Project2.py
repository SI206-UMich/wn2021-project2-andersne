from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    soup = BeautifulSoup(filename, 'html.parser')
    title_tags = soup.find_all('a', class_="bookTitle")
    author_tags = soup.find_all('a', class_="authorName")
    title_list = []
    author_list = []
    final = []

    for tag in title_tags:
        titles = tag.find('span')
        for title in titles:
            title_list.append(title.strip())

    for tag in author_tags:
        authors = tag.find('span')
        for author in authors:
            author_list.append(author.strip())

    for i in range(len(title_list)):
        final.append((title_list[i], author_list[i]))

    return final


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    r = requests.get('https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc')
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.find_all('a', class_='bookTitle')
    urls = []
    for tag in tags: 
        href = tag.get('href')
        urls.append('https://www.goodreads.com'+href)
    return urls[:10]


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text,'html.parser')

    title_tag = soup.find('h1', id='bookTitle')
    for tag in title_tag:
        title = tag.strip()

    name_tag = soup.find('span', itemprop='name')
    for tag in name_tag:
        name = tag.strip()

    pages_tag = soup.find('span',itemprop='numberOfPages')
    for pages in pages_tag:
        page_string = pages
    page_count = int(page_string.split(' ')[0])

    return (title, name, page_count)

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    soup = BeautifulSoup(filepath, 'html.parser')
    title_tags = soup.find_all('img', class_='category__winnerImage')
    titles = []
    for tag in title_tags: 
        title = tag.get('alt')
        titles.append(title.strip())

    category_tags = soup.find_all('h4', class_='category__copy')
    categories = []
    for tag in category_tags:
        for category in tag:
            categories.append(category.strip())

    url_tags = soup.find_all('div', class_='category clearFix')
    urls =[]
    for tag in url_tags:
        url = tag.find_all('a')
        for i in url:
            var1 = i.get('href')
            if var1!= 'https://www.goodreads.com/choiceawards/best-books-2020#':
                urls.append(var1.strip())
    final = []
    for i in range(len(titles)):
        final.append((categories[i], titles[i], urls[i]))

    return final

file = open('best_books_2020.htm','r')
summarize_best_books(file)
file.close()

def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    pass


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls


    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        file = open('search_results.htm', 'r')
        test = get_titles_from_search_results(file)
        file.close()

        # check that the number of titles extracted is correct (20 titles)
        self.assertTrue(len(test) == 20)

        # check that the variable you saved after calling the function is a list
        self.assertTrue(type(test) == list)

        # check that each item in the list is a tuple
        for i in test:
            self.assertTrue(type(i) == tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(test[0],('Harry Potter and the Deathly Hallows (Harry Potter, #7)','J.K. Rowling'))

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(test[19][0],'Harry Potter: The Prequel (Harry Potter, #0.5)')

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        test = get_search_links()
        self.assertEqual(type(test), list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(test), 10)

        # check that each URL in the TestCases.search_urls is a string
        for url in test:
            self.assertTrue(type(url)==str)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show
        for url in test:
            self.assertTrue(url.startswith('https://www.goodreads.com/book/show/'))

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in get_search_links():
            summaries.append(get_book_summary(url))

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries),10)

        # check that each item in the list is a tuple
        for i in summaries:
            self.assertTrue(type(i) == tuple)

        # check that each tuple has 3 elements
        for i in summaries:
            self.assertEqual(len(i), 3)

        # check that the first two elements in the tuple are string
        for i in summaries:
            self.assertTrue(type(i[0]) == str)
            self.assertTrue(type(i[1]) == str)

        # check that the third element in the tuple, i.e. pages is an int
        for i in summaries:
            self.assertTrue(type(i[2]) == int)

        # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        file = open('best_books_2020.htm','r')
        best_books = summarize_best_books(file)
        file.close()

        # check that we have the right number of best books (20)

        self.assertEqual(len(best_books),20)

            # assert each item in the list of best books is a tuple
        for i in best_books:
            self.assertTrue(type(i)==tuple) 
            # check that each tuple has a length of 3
            self.assertEqual(len(i),3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0],('Fiction', 'The Midnight Library', 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[len(best_books)-1],('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable

        # call write csv on the variable you saved and 'test.csv'

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)


        # check that there are 21 lines in the csv

        # check that the header row is correct

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'

        return None

if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)




