import json
import requests

cookies = {
    'client_id': 'eyJpdiI6Ill5YVRvYStEYTNRd2FnS0ZvNi91emc9PSIsInZhbHVlIjoidGIwQnI2TE5zTjZGR2hHYWpubmhwdGZPRTcvQTFkb1lLUGdoZ09wa0t0YWpCcnkrajcxck9rTmN5RUpiNER6SWZJUzY3QUV5c21YUTBxdU1DRTg3QkE9PSIsIm1hYyI6IjlkYjg5MjE4Yzc3YzUwYmRhZjM2MGVhMDg5YjE5NTBmNTc1ZGNmYmVmNTZhNmRhOTAzNDY5OWM1YTZjYTJmN2YiLCJ0YWciOiIifQ%3D%3D',
    'cookiesAccepted': 'true',
    '_gid': 'GA1.3.2032047982.1703004649',
    '_ga': 'GA1.3.884276600.1703004649',
    'XSRF-TOKEN': 'eyJpdiI6Ik1FV0JOR2l4TFIvQ1Z1bytJSnpRMHc9PSIsInZhbHVlIjoiQnZxbDJyZGdiMjVLS2VQWVdmTmIvbEVaZ2dZTUh3bXljZTJaUXlBSTY5VGRTQ1ZvamIwQkpmdlg4R05zK1gxblFJMisyT0Y0cVJTQnJjc3pTajhRQzI0WjRoK2RPOE10azg0K3RTeER2a1Bid1RvNUJlNlV6c1ZJbnBDbVpDWGMiLCJtYWMiOiIxMzI5N2MzZDEwNDhiNDBkMTgxYzhlYTFkNzc5YjE1NThlMmU1ZGNhMDAyNmE4MjhjZTYzNDBmMWQ4Y2FjZDM0IiwidGFnIjoiIn0%3D',
    'laravel_session': 'eyJpdiI6Ik4yRGNVNmJzdGFTaWFHT1doejN6SUE9PSIsInZhbHVlIjoiaHNyVzJ4ajhhdXVrTFpKZ1N5clVyb3l2V2M0bUdPY1Rma1ZNV284TEJsU1hQWlRUSFRQSUpjaUtyRkxtWm1QcXNHNUVBUHpkc3BpNDdBMVFacGJMbEJ0bFBuU1FuaW5Td0hEMGJEUGhjRzVHZFI0dURPNHhuNHJwVnhYQytOanUiLCJtYWMiOiI1YzE2NDVmM2VhMTc0YTZhMTNmYTMzMzc2MDAzN2VmZmE2NGRlYTdkMGQ4YmRiMWU3NDExOTJhNjExZjcxMjliIiwidGFnIjoiIn0%3D',
    'last_query': 'eyJpdiI6Ikkxc0M5SnU2M284QnpaY3dYVmFQZ3c9PSIsInZhbHVlIjoiZ1dGQjJUamlzeDdWS0VPMUxjNnJwN0N2QlVKUGFuRm1qd0RnWHkxVkF5OW02WnBod3Z1MnQ2VE55dUxHSTZaczVsWWhUamlQdkZYUXNMbWNYckhYOHc9PSIsIm1hYyI6IjkxZTgxOWU5YTA5MTVmMWQ2Yzk0YTA1MDNmM2Y3NzM5NWU4ODJlYzM5ZGJjMWE3NGFmOWQ3NDIyNWQ5NDhlMTQiLCJ0YWciOiIifQ%3D%3D',
    '_ga_YFS57NGF8S': 'GS1.1.1703004649.1.1.1703005286.60.0.0',
}

headers = {
    'authority': 'adviserbook.co.uk',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': 'client_id=eyJpdiI6Ill5YVRvYStEYTNRd2FnS0ZvNi91emc9PSIsInZhbHVlIjoidGIwQnI2TE5zTjZGR2hHYWpubmhwdGZPRTcvQTFkb1lLUGdoZ09wa0t0YWpCcnkrajcxck9rTmN5RUpiNER6SWZJUzY3QUV5c21YUTBxdU1DRTg3QkE9PSIsIm1hYyI6IjlkYjg5MjE4Yzc3YzUwYmRhZjM2MGVhMDg5YjE5NTBmNTc1ZGNmYmVmNTZhNmRhOTAzNDY5OWM1YTZjYTJmN2YiLCJ0YWciOiIifQ%3D%3D; cookiesAccepted=true; _gid=GA1.3.2032047982.1703004649; _ga=GA1.3.884276600.1703004649; XSRF-TOKEN=eyJpdiI6Ik1FV0JOR2l4TFIvQ1Z1bytJSnpRMHc9PSIsInZhbHVlIjoiQnZxbDJyZGdiMjVLS2VQWVdmTmIvbEVaZ2dZTUh3bXljZTJaUXlBSTY5VGRTQ1ZvamIwQkpmdlg4R05zK1gxblFJMisyT0Y0cVJTQnJjc3pTajhRQzI0WjRoK2RPOE10azg0K3RTeER2a1Bid1RvNUJlNlV6c1ZJbnBDbVpDWGMiLCJtYWMiOiIxMzI5N2MzZDEwNDhiNDBkMTgxYzhlYTFkNzc5YjE1NThlMmU1ZGNhMDAyNmE4MjhjZTYzNDBmMWQ4Y2FjZDM0IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6Ik4yRGNVNmJzdGFTaWFHT1doejN6SUE9PSIsInZhbHVlIjoiaHNyVzJ4ajhhdXVrTFpKZ1N5clVyb3l2V2M0bUdPY1Rma1ZNV284TEJsU1hQWlRUSFRQSUpjaUtyRkxtWm1QcXNHNUVBUHpkc3BpNDdBMVFacGJMbEJ0bFBuU1FuaW5Td0hEMGJEUGhjRzVHZFI0dURPNHhuNHJwVnhYQytOanUiLCJtYWMiOiI1YzE2NDVmM2VhMTc0YTZhMTNmYTMzMzc2MDAzN2VmZmE2NGRlYTdkMGQ4YmRiMWU3NDExOTJhNjExZjcxMjliIiwidGFnIjoiIn0%3D; last_query=eyJpdiI6Ikkxc0M5SnU2M284QnpaY3dYVmFQZ3c9PSIsInZhbHVlIjoiZ1dGQjJUamlzeDdWS0VPMUxjNnJwN0N2QlVKUGFuRm1qd0RnWHkxVkF5OW02WnBod3Z1MnQ2VE55dUxHSTZaczVsWWhUamlQdkZYUXNMbWNYckhYOHc9PSIsIm1hYyI6IjkxZTgxOWU5YTA5MTVmMWQ2Yzk0YTA1MDNmM2Y3NzM5NWU4ODJlYzM5ZGJjMWE3NGFmOWQ3NDIyNWQ5NDhlMTQiLCJ0YWciOiIifQ%3D%3D; _ga_YFS57NGF8S=GS1.1.1703004649.1.1.1703005286.60.0.0',
    'origin': 'https://adviserbook.co.uk',
    'referer': 'https://adviserbook.co.uk/financial-adviser/s/LE19+1WL?dist=50&investments=1&page=4',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-xsrf-token': 'eyJpdiI6Ik1FV0JOR2l4TFIvQ1Z1bytJSnpRMHc9PSIsInZhbHVlIjoiQnZxbDJyZGdiMjVLS2VQWVdmTmIvbEVaZ2dZTUh3bXljZTJaUXlBSTY5VGRTQ1ZvamIwQkpmdlg4R05zK1gxblFJMisyT0Y0cVJTQnJjc3pTajhRQzI0WjRoK2RPOE10azg0K3RTeER2a1Bid1RvNUJlNlV6c1ZJbnBDbVpDWGMiLCJtYWMiOiIxMzI5N2MzZDEwNDhiNDBkMTgxYzhlYTFkNzc5YjE1NThlMmU1ZGNhMDAyNmE4MjhjZTYzNDBmMWQ4Y2FjZDM0IiwidGFnIjoiIn0=',
}

json_data = {
    'data': {
        'pcds': {
            'longitude': -1.190872,
            'latitude': 52.601674,
        },
        'method': 'postcode',
        'query': 'LE19 1WL',
        'orig_query': 'LE191WL',
        'dist': 50,
    },
    # '_token': 'ilufktFuZdfXiCgoSrnFZY8LXFPavnG211JUwzmv',
}

response = requests.post('https://adviserbook.co.uk/search/get-results', cookies=cookies, headers=headers, json=json_data)
print(response.content)
# print(response.content)
# data = response.json()  # This will give you a Python dictionary

#     # Write the JSON data to a file
# with open('tests/a_adviserbook/output.json', 'w', encoding='utf-8') as file:
#     json.dump(data, file, indent=4)
# html = response.content
# string_content = html.decode('utf-8')

# # output = response.content

# with open('tests/a_adviserbook/output.json', 'w', encoding='utf-8') as file:
#     file.write(json.dumps(string_content, indent=4))