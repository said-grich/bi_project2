import json
import time

from BookingScript import BookingScript
from GooglemapsScript import GoogleMapsScript

if __name__ == '__main__':
    hotel_name=str(input("donner les nome"));
    scriptboocking = BookingScript();
    scriptboocking.fill_form(hotel_name);
    accommodations_data = scriptboocking.scrape_accommodation_data();
    with open(hotel_name+"booking.json", 'w') as f:
         json.dump(accommodations_data, f)
    time.sleep(5);
    scriptGoogleMaps =GoogleMapsScript();
    scriptGoogleMaps.fill_form(hotel_name);
    accommodations_data = scriptGoogleMaps.scrape_accommodation_data();
    with open(hotel_name+"googleMaps.json", 'w') as f:
         json.dump(accommodations_data, f)

