import subprocess
import re
import time
import os
from concurrent.futures import ThreadPoolExecutor

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 80

def show_animated_logo():
    width = get_terminal_width()
    RED = "\033[91m"
    RESET = "\033[0m"
    
    logo = [
        r"          _  __    __    _      _   _ ",
        r" \ \      / /|  ___|/ ___|  / ___|  / \\    | \\ | |",
        "  \\ \\ /\\ / / | |_   \\___ \\ | |     / _ \\   |  \\| |",
        "   \\ V  V /  |  _|   _) || |_ / ___ \\  | |\\  |",
        "    \\_/\\_/   |_|    |____/  \\____/_/   \\_\\ |_| \\_|",
        "                                                  ",
        "      [ WIRELESS & FREQUENCY NETWORK SCANNER ]   "
    ]
    
    print("\n")
    for line in logo:
        centered_line = line.center(width)
        print(f"{RED}{centered_line}{RESET}")
        time.sleep(0.04)
        
    divider = ("=" * 51).center(width)
    print(f"\n{RED}{divider}{RESET}\n")

def check_single_device(ip):
    deep_cmd = ["sudo", "nmap", "-O", "-p", "22,80,443,139,445,5353,62078", "-T5", "--max-rtt-timeout", "500ms", "--osscan-limit", ip]
    try:
        scan_res = subprocess.run(deep_cmd, capture_output=True, text=True, timeout=12)
        stdout = scan_res.stdout
        stdout_lower = stdout.lower()
        
        hostname = "Unknown"
        
        vendor = "Unknown"
        mac_match = re.search(r"MAC Address: [0-9A-F:]+ \(([^)]+)\)", stdout)
        if mac_match:
            vendor = mac_match.group(1)

        os_ver = "Unknown Device"
        os_match = re.search(r"OS details: ([^\n]+)", stdout)
        
        if os_match:
            os_ver = os_match.group(1)
            os_ver = re.sub(r"\(build [^)]+\)", "", os_ver).strip()
        else:
            vendor_lower = vendor.lower()
            android_brands = [
                "samsung", "xiaomi", "huawei", "redmi", "poco", 
                "oneplus", "google", "oppo", "vivo", "realme", 
                "motorola", "meizu", "hmd global", "lenovo", "lg "
            ]
            
            if "62078/tcp open" in stdout_lower or "apple-mobdev" in stdout_lower or "apple" in vendor_lower:
                os_ver = "iOS (iPhone/iPad)"
            elif any(brand in vendor_lower for brand in android_brands) or "android" in stdout_lower:
                os_ver = "Android OS"
            elif "445/tcp open" in stdout_lower or "139/tcp open" in stdout_lower:
                os_ver = "Windows OS"
            elif "22/tcp open" in stdout_lower:
                os_ver = "Linux OS"
            elif "80/tcp open" in stdout_lower or "443/tcp open" in stdout_lower:
                if "tp-link" in vendor_lower:
                    os_ver = "Router / AP (Linux)"
                else:
                    os_ver = "Network Device"

        print(f"[+] Scanned: {ip:<15} | OS: {os_ver[:25]}")
        return {"ip": ip, "name": hostname, "vendor": vendor, "os": os_ver}
    except Exception:
        return {"ip": ip, "name": "Unknown", "vendor": "Unknown", "os": "Timeout"}

def main():
    show_animated_logo()
    
    networks = ["10.0.0.0/24", "192.168.100.0/24"]
    all_ips = []
    
    print("=== STEP 1: Fast Active IP Discovery ===")
    for net in networks:
        ping_cmd = ["sudo", "nmap", "-sn", net]
        try:
            res = subprocess.run(ping_cmd, capture_output=True, text=True, check=True)
            found_ips = re.findall(r"Nmap scan report for (?:[a-zA-Z0-9.-]+ )?\(?([0-9.]+)\)?", res.stdout)
            all_ips.extend(found_ips)
        except Exception as e:
            print(f"[-] Network scan error {net}: {e}")
            
    print(f"[+] Found {len(all_ips)} active IPs. Launching parallel OS analysis...\n")
    
    with ThreadPoolExecutor(max_workers=25) as executor:
        results = executor.map(check_single_device, all_ips)
        all_devices = list(results)

    if all_devices: 
        header = f"{'No':<3} | {'IP Address':<15} | {'Vendor':<15} | {'OS / Version':<25}"
        separator = "-" * len(header)
        print("\n=== FINAL DEVICE LIST ===")
        print(header)
        print(separator)
        for idx, dev in enumerate(all_devices, 1):
            vendor_short = dev['vendor'][:13] + '..' if len(dev['vendor']) > 15 else dev['vendor']
            os_short = dev['os'][:23] + '..' if len(dev['os']) > 25 else dev['os']
            print(f"[{idx:<1}] | {dev['ip']:<15} | {vendor_short:<15} | {os_short:<25}")
        print(separator)
    else:
        print("[-] No devices found.")

if __name__ == "__main__":
    main()
input("Press Enter to exit...")
