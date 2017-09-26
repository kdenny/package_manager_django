import requests

url = 'http://packagerat.pythonanywhere.com/packages/'

package_data = [{

    'recipient': 1,
    'apartment_no': '309',
    'package_type': 'small',
    'status': 'pending'
}]

r = requests.post(url, json = package_data)
print(r.text)

