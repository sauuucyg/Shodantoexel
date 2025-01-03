import shodan
import openpyxl

# Shodan API key
API_KEY = "" # Enter your Shodan API key

# Public IP addresses to scan
ip_addresses = [
    "", # Enter the public IP addresses to be scanned
    "", # Enter the public IP addresses to be scanned
    "", # Enter the public IP addresses to be scanned
    ""  # Enter the public IP addresses to be scanned
# ...
]

# Create a new Excel workbook
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Shodan Scan Results"

# Add headers to the sheet
sheet.append(["IP Address", "Open Ports", "Service Details"])

# Function to scan open ports
def scan_ports(api_key, ip_address):
    api = shodan.Shodan(api_key)

    try:
        # Search for IP address information
        host = api.host(ip_address)

        # Collect open ports and service details
        open_ports = []
        service_details = []
        for service in host['data']:
            open_ports.append(str(service['port']))
            details = f"Port: {service['port']}, Service: {service['transport']}, Product: {service.get('product', 'Unknown')}, Version: {service.get('version', 'Unknown')}"
            service_details.append(details)

        # Convert lists to strings
        open_ports_str = ", ".join(open_ports)
        service_details_str = " | ".join(service_details)

        # Print and save results
        print(f"Open ports for IP address {ip_address}: {open_ports_str}")
        sheet.append([ip_address, open_ports_str, service_details_str])

    except shodan.APIError as e:
        print(f"Error for IP address {ip_address}: {e}")

# Loop over IP addresses
for ip_address in ip_addresses:
    scan_ports(API_KEY, ip_address)

# Save the Excel file
workbook.save("shodan_scan_results.xlsx")
print("Results have been saved to shodan_scan_results.xlsx.")
