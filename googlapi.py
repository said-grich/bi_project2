from outscraper import ApiClient

api_cliet = ApiClient(api_key='AIzaSyDtrJaqloJsrA8qGKs2OrNcDzXamnaYabM')
reviews_response = api_cliet.google_maps_business_reviews('Golden Unicorn, East Broadway, USA')