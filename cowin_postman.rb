require 'uri'
require 'net/http'

url = URI("https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=314&date=20-05-2021")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(url)
request["cache-control"] = 'no-cache'
# request["postman-token"] = '6aa89728-0e0c-bd32-49b2-0772f5eb7d40'

response = http.request(request)
puts response.read_body

url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=314&date=20-05-2021'
RestClient.get(url)
results = JSON.parse(res)

availability = {}
result[:centers].each do |center|
  # 1st condition - Checking Age
  sessions = center[:sessions].select{ |c| c[:min_age_limit] == 18 }
  # 2nd condition - Checking Availability
  sessions_with_availability = sessions.select{ |s| s[:available_capacity] > 0 }
  # Collect date for specific pincode if there's vaccine availability
  availability[center[:pincode]] = sessions_with_availability.collect{ |s| s[:date] } if sessions_with_availability.any?
end

puts availability