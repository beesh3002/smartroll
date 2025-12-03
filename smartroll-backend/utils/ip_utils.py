from flask import request, current_app

def client_ip():
    """
    Returns the client's IP address.
    In the future, if the app is behind a proxy (like Nginx or Cloud), 
    it can extract the real IP from headers.
    """
    return request.headers.get("X-Forwarded-For", request.remote_addr) or "0.0.0.0"


def get_ip_prefix():
    """
    Extracts the first two segments (network prefix) from the IP address.
    Example:
        192.168.10.24 -> "192.168."
        10.255.136.4  -> "10.255."
    This helps identify which classroom Wi-Fi subnet the device is connected to.
    """
    ip = client_ip()
    parts = ip.split(".")
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}."
    return ip


def on_class_wifi():
    """
    Legacy helper — keeps backward compatibility with earlier logic.
    Still checks if the IP prefix matches any configured classroom subnet
    in app.config["CLASS_WIFI_SUBNETS"] (defined in .env as CLASS_WIFI_SUBNETS=10.,192.168.)
    """
    ip = client_ip()
    for prefix in current_app.config.get("CLASS_WIFI_SUBNETS", []):
        if ip.startswith(prefix):
            return True
    return False
