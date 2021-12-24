import json

from BookingScript import BookingScript

if __name__ == '__main__':
    scriptboocking = BookingScript();
    scriptboocking.fill_form("Aqua Mirage Club");
    accommodations_data = scriptboocking.scrape_accommodation_data();
    with open('booking_data.json', 'w') as f:
        json.dump(accommodations_data, f)

