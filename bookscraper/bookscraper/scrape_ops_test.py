import requests

response = requests.get(
  url='https://headers.scrapeops.io/v1/user-agents',
  params={
      'api_key': '2bb9eaa3-b008-48df-98fa-6b175af37535',
      'num_results': '2'}
)

print('Response Body: ', response.json())
