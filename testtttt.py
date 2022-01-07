import requests as r

if __name__ == '__main__':
    rq=r.get("https://uk.trustpilot.com/_next/data/businessunitprofile-consumersite-2005/review/www.little-mouse.co.uk.json?page=1&businessUnit=www.little-mouse.co.uk")
    data=rq.json()
    print(data)

