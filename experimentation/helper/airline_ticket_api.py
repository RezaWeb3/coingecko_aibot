ticket_prices = {"london":"$799", "dubai":"$1200", "nyc":"$199"}

def getTicketPrice(city):
    city = str.lower(city)
    return ticket_prices.get(city, "unknown")


