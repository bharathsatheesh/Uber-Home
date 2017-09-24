from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from geolocation.main import GoogleMaps
from operator import itemgetter
from geopy.geocoders import Nominatim
from geocodio import GeocodioClient
# import find_loc

def return_latlng(enquiry):
    address = enquiry

    google_maps = GoogleMaps(api_key='AIzaSyCw6c6wq-VY06rOn401rwtv-Q7MU3-C89M') 

    location = google_maps.search(location=address) # sends search to Google Maps.

    # print(location.all()) # returns all locations.

    my_location = location.first() # returns only first location.

    # route_name = my_location.route
    # st = my_location.street_number
    # place = my_location.formatted_address

    # print(route_name)
    # print(my_location.lng)
    # print(my_location.street_number)
    # print(my_location.formatted_address)

    # lat = 37.751502
    # lng = -122.386707

    # my_location = google_maps.search(lat=lat, lng=lng).first()
    # print (my_location.route)
    return [my_location.lat, my_location.lng]

def locate_spot(coods):
    geolocator = Nominatim()
    lat = coods[0]
    lng = coods[1]
    # client = GeocodioClient('3764147741b0c1b3b95697f495fcf64911c4c51')
    # location = client.reverse(coods)
    # return location.formatted_address

    loc_string = str(lat) + ', ' +str(lng) 
    location = geolocator.reverse(loc_string)
    return location.address

    # print ((lat,lng))
    # google_maps = GoogleMaps(api_key='AIzaSyCw6c6wq-VY06rOn401rwtv-Q7MU3-C89M') 
    # flag = True
    # while flag:
    #     my_location = google_maps.search(lat=lat, lng=lng).first()
    #     destination = my_location.formatted_address
    #     if ((destination.split())[0]).isdigit():
    #         print (destination)
    #         flag = False

def find_optimal_pickup(start,end):
    session = Session(server_token='ZX14_Gl4xEJcQLXyLGT_OBYVRoJXJL0tXB4ijyPp')
    client = UberRidesClient(session)

    # Get price and time estimates
    response = client.get_products(37.77, -122.41)
    products = response.json.get('products')

    pickup = start
    [pick_lat,pick_lng] = return_latlng(pickup)

    dropoff = end
    [drop_lat,drop_lng] = return_latlng(dropoff)

    pickup_list = [[pick_lat,pick_lng]]
    dropoff_list = [[drop_lat,drop_lng]]
    diff = 0.0003

    for i in range(1, 20):
        lat_diff = pick_lat - i*diff
        lng_diff = pick_lng - i*diff
        pickup_list.append([lat_diff,pick_lng])
        pickup_list.append([pick_lat,lng_diff])

    for i in range(1, 20):
        lat_diff = pick_lat + i*diff
        lng_diff = pick_lng + i*diff
        pickup_list.append([lat_diff,pick_lng])
        pickup_list.append([pick_lat,lng_diff])

    # print (my_pickup.lat,my_pickup.lng,my_dropoff.lat,my_dropoff.lng)
    cost_list = []
    ctr = 0
    for [pick_lat,pick_lng] in pickup_list:
        response = client.get_price_estimates(
            start_latitude=pick_lat,
            start_longitude=pick_lng,
            
            end_latitude=drop_lat,
            end_longitude=drop_lng,
            seat_count=1
        )

        estimate = response.json.get('prices')
        for element in estimate:
            if element['localized_display_name'] == 'POOL':
                cost_list.append([(element['low_estimate']+element['high_estimate'])/2, [pick_lat,pick_lng]])
                ctr += 1
    cost_list.sort()
    print (cost_list)
    [cost, [lat,lng]] = cost_list[0]
    print([lat,lng])
    print (cost)
    return locate_spot((lat,lng))


# start = "Newport Centre, NJ"
# end = "Portside Towers Apartments"
# find_optimal_pickup(start,end)