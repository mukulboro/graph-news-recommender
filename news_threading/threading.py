from concurrent.futures import ThreadPoolExecutor

class ThreadScraping:
    def run(self,**kwargs):
        """
        Receives a dictionary of objects and runs the get_all_news method of each object in a separate thread.

        Use Case:
        ---------
        Suppose we have multiple scraper objects, each responsible for scraping news from a specific website. 
        You can use this class to execute the `get_all_news` method of each scraper object concurrently.
        *****each scraper object must have a method named `get_all_news`*****
        Example:
        --------
        scraper1 = NewsScraper1("Website1")
        scraper2 = NewsScraper2("Website2")
        scraper3 = NewsScraper3("Website3")

        thread_scraping = ThreadScraping()
        results = thread_scraping.run(website1=scraper1, website2=scraper2, website3=scraper3)

        # Output: {'website1': 'scraped news from Website1', 
        #          'website2': 'scraped news from Website2', 
        #          'website3': 'scraped news from Website3'}



        """
        results={}
        with ThreadPoolExecutor() as executor:
            futures = {website: executor.submit(obj.get_all_news) for website, obj in kwargs.items()}

            for website, future in futures.items():
                results[website] = future.result()

        return results