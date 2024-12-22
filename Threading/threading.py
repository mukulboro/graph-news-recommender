from concurrent.futures import ThreadPoolExecutor

class ThreadScraping:
    def run(self,**kwargs):
        """
        Receives a dictionary of objects and runs the get_all_news method of each object in a separate thread.
        """
        results={}
        with ThreadPoolExecutor() as executor:
            futures = {website: executor.submit(obj.get_all_news) for website, obj in kwargs.items()}

            for website, future in futures.items():
                results[website] = future.result()

        return results