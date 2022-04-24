### Test Yelp
import json
import requests
headers = {'Authorization': 'Bearer %s' % 'boovLwU4BPpx-X7tEPWSbQvHQkkAGp_g3lHxukYM9SAGtgWpkrkRc-VKL-HddKAAU34rF84x_2Ji301y470F6GwaXjAxUMtslVfNsamfSpLbkiuPDllhszvP3AxOYnYx'}
response = requests.get("https://api.yelp.com/v3/businesses/search?location=1695 Broadway Street, Ann Arbor, MI&categories=chinese,indian&price=2", headers=headers)
#
json_str = response.text  # JSON string
info_list = json.loads(json_str)
print(info_list)
info_list_key = info_list.keys()
print(info_list_key)
info_business = info_list["businesses"][0]
info_business_key = info_business.keys()
print(info_business_key)





# ### Test Doordash
# # Generate token
# import jwt.utils
#
# import time
# import math
#
# token = jwt.encode(
#     {
#         "aud": "doordash",
#         "iss": "56170aa2-d111-49a7-8490-f8dcca7aee5f",
#         "kid": "9e186004-7e27-46ca-9e47-3b253282fe7c",
#         "exp": str(math.floor(time.time() + 60)),
#         "iat": str(math.floor(time.time())),
#     },
#     jwt.utils.base64url_decode("-8VobQrVCQanf6RBK5fsk525d8BptDdWi9VsxrN8geo"),
#     algorithm="HS256",
#     headers={"dd-ver": "DD-JWT-V1"})
#
# # Generate delivery
# import requests
# import uuid
#
# endpoint = "https://openapi.doordash.com/drive/v2/deliveries/" # DRIVE API V2
#
# headers = {"Authorization": "Bearer " + token,
#             "Content-Type": "application/json"}
#
# delivery_id = str(uuid.uuid4()) # Randomly generated UUID4
#
# request_body = { # Modify pickup and drop off addresses below
#     "external_delivery_id": delivery_id,
#     "pickup_address": "901 Market Street 6th Floor San Francisco, CA 94103",
#     "pickup_business_name": "Wells Fargo SF Downtown",
#     "pickup_phone_number": "+16505555555",
#     "pickup_instructions": "Enter gate code 1234 on the callbox.",
#     "dropoff_address": "901 Market Street 6th Floor San Francisco, CA 94103",
#     "dropoff_business_name": "Wells Fargo SF Downtown",
#     "dropoff_phone_number": "+16505555555",
#     "dropoff_instructions": "Enter gate code 1234 on the callbox.",
#     "order_value": 1999
# }
#
# create_delivery = requests.post(endpoint, headers=headers, json=request_body) # Create POST request
#
#
# # print(create_delivery.status_code)
# # print(create_delivery.text)
# # print(create_delivery.reason)
#
# # Check delivery status
# import requests
# import uuid
#
# endpoint = "https://openapi.doordash.com/drive/v2/deliveries/" # DRIVE API V2
#
# headers = {"Authorization": "Bearer " + token,
#             "Content-Type": "application/json"}
#
# get_delivery = requests.get(endpoint + 'cca0d7cf-6809-497d-96a6-a78aff6c8954', headers=headers) # Create GET request
#
# print(get_delivery.status_code)
# print(get_delivery.text)
# print(get_delivery.url)




# ## Test fatsecretPlatform
# from fatsecret import Fatsecret
#
# fs = Fatsecret(consumer_key='97bfcb08999645158c288ba91346f5c6', consumer_secret='ac06fa6b3aa249e1b3b88242c6ffd7e1')
# foods = fs.foods_search("Beef Dumpling Soup")
#
# print(foods)

