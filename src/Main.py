import requests
import json
# from GmailWorker import send_email
# from WaitUtils import wait_minutes
from utils.GmailWorker import send_email
from utils.WaitUtils import wait_minutes

import argparse

# https://pay.planetakino.ua/api/v1/cart/show-times?showTimeId=454215&theaterId=pk-kharkov&includeSeats=y&includeDetail=y
def genExpectedSeats(rows, places):
    result_list = []
    for row in rows:
        for place in places:
            result_list.append(str(row * 100000 + place))
    return result_list

def findSeats(emptySeats, expectedSeats):
    foundSeats = []
    for seat in expectedSeats:
        if (seat in emptySeats):
            foundSeats.append(seat)
    return foundSeats


def differWithPrevious(prev, new):
    sorted_prev = sorted(prev)
    sorted_new = sorted(new)
    print("sorted prev: {0}".format(sorted_prev))
    print("sorted new: {0}".format(sorted_new))

    return sorted_prev != sorted_new


def doAll(previous_res, movie_id):
    # movie_id=movie_id
    seats_request = "https://pay.planetakino.ua/api/v1/cart/halls?showtimeId={0}".format(movie_id)
    movie_link="https://pay.planetakino.ua/hall/pk-kharkov/{0}".format(movie_id)
    print("Sending seats request")
    response = requests.get(seats_request)
    assert response.status_code == 200
    print("response 200")

    print("Parsing json")
    parsed_json = json.loads(response.text)

    emptySeats = parsed_json['data']['hallsSheme'][0]['emptySeats']
    print("Parsed. Empty seats {0}".format(len(emptySeats)))

    # emptySeats = ['1000001', '1000002', '1000003', '1000026', '1000027', '1000028', '1000029', '1100026', '1100027', '1100028', '1100029', '1200001', '1200002', '1200003', '1200004', '1200005', '1200025', '1200026', '1200027', '1200028', '1200029', '1300001', '1300002', '1300003', '1300004', '1300005', '1300006', '1300007', '1300008', '1300009', '1300030', '1300031', '1300032', '1300033', '1300034', '1300035', '1300036', '1300037', '1300038', '300007', '300008', '300009', '300010', '300011', '300012', '300013', '300014', '300015', '300016', '300017', '300018', '300019', '300020', '300021', '300022', '300023', '300024', '300025', '300026', '300027', '300028', '300029', '300030', '400001', '400002', '400003', '400004', '400005', '400006', '400007', '400008', '400009', '400010', '400011', '400012', '400013', '400025', '400026', '400027', '400028', '400029', '400030', '400031', '400032', '400033', '400034', '400035', '400036', '500001', '500002', '500003', '500004', '500005', '500006', '500007', '500008', '500029', '500030', '500031', '500032', '500033', '500034', '500035', '500036', '600001', '600002', '600003', '600004', '600005', '600006', '600007', '600008', '600029', '600030', '600031', '600032', '600033', '600034', '600035', '600036', '700001', '700002', '700003', '700004', '700026', '700027', '700028', '700029', '800001', '800002', '800003', '800004', '800027', '800028', '800029', '900001', '900002', '900003', '900006', '900026', '900027', '900028', '900029']

    print("Searching for suitable available seats:")

    rows  = range(7,12)
    places = range(7,22)

    expectedSeats = genExpectedSeats(rows, places)
    availableSeats = findSeats(emptySeats, expectedSeats)
    print("available seats: {0}".format(availableSeats))

    if availableSeats:
        if differWithPrevious(previous_res, availableSeats):
            send_email("alex.cherevatiy@gmail.com", "Found [{0}] seats for you".format(len(availableSeats)),
                               createBody(availableSeats, movie_link))
        else:
            print("No difference found with previous list")

    else:
        print("No available seats found, not sending email")
    return availableSeats

def createBody(seatsList, movie_link):
    res = "Found {0} available seats.\nList of seats: {1}.\nLink to movie: [{2}]\n".format(len(seatsList), seatsList, movie_link)
    return res

def read_cmd_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--showId', '-sid', help='please set tje show id using rather "-sid" or "--showId"', required=True)
    return parser.parse_args()

if __name__ == '__main__':
    iteration = 1
    previous_results = []
    args = read_cmd_arguments()
    movie_id = args.showId
    print(movie_id)

    while True:
        print("Iteration {0}".format(iteration))
        try:
            previous_results = doAll(previous_results, movie_id)
        except Exception as e:
            print("Exception caught!!!")
            print(e)
        # wait_minutes(0.1)
        wait_minutes(0.5)
        iteration += 1