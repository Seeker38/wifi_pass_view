import subprocess

try:
    meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], shell=True)
    data = meta_data.decode('utf-8', errors="backslashreplace")
    data = data.split('\n')
    profiles = []

    for i in data:
        if "All User Profile" in i:
            i = i.split(":")[1].strip()
            profiles.append(i)

    print("{:<30} | {:<}".format("Wi-Fi Name", "Password"))
    print("________________________________________________")

    for profile in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], shell=True)
            results = results.decode('utf-8', errors="backslashreplace")
            results = results.split('\n')
            password = [b.split(":")[1].strip() for b in results if "Key Content" in b]

            try:
                print("{:<30} | {:<}".format(profile, password[0]))
            except IndexError:
                print("{:<30} | {:<}".format(profile, ""))

        except subprocess.CalledProcessError:
            print("Error occurred while retrieving data for '{}'".format(profile))

except subprocess.CalledProcessError:
    print("Error occurred while retrieving Wi-Fi profiles")