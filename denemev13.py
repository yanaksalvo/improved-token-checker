import requests
import time
from datetime import datetime, timezone

valid_tokens = []
invalid_tokens = []
locked_tokens = []
unknown_tokens = []
no_nitro_tokens = []
nitro_classic_tokens = []
nitro_boost_tokens = []
verified_true_tokens = []
verified_false_tokens = []
phone_true_tokens = []
phone_false_tokens = []
email_tokens = []
payment_tokens = []

Discord_Employee = 1
Partnered_Server_Owner = 2
HypeSquad_Events = 4
Bug_Hunter_Level_1 = 8
House_Bravery = 64
House_Brilliance = 128
House_Balance = 256
Early_Supporter = 512
Bug_Hunter_Level_2 = 16384
Early_Verified_Bot_Developer = 131072
No_Badge = 0

threads = int(input("Threads > "))

with open("tokens.txt") as f:
    tokens = f.readlines()

start_time = time.time()

for token in tokens:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Authorization": token.strip()
    }
    try:
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data["id"]
            username = user_data["username"]
            discriminator = user_data["discriminator"]
            locale = user_data.get("locale", "Not Available")
            nsfw_allowed = user_data.get("nsfw_allowed", False)
            mfa_enabled = user_data.get("mfa_enabled", False)
            creation_date = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            premium_type = user_data.get("premium_type", 0)
            verified = user_data.get("verified", False)
            phone = user_data.get("phone", None)
            email = user_data.get("email", None)
            banner_url = f"https://cdn.discordapp.com/banners/{user_id}/{user_data.get('banner', 'default_banner_id')}.png"
            avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_data.get('avatar', 'default_avatar_id')}.png"

           
            servers_response = requests.get(f"https://discord.com/api/v9/users/@me/guilds", headers=headers)
            friends_response = requests.get(f"https://discord.com/api/v9/users/@me/relationships", headers=headers)
            badges_response = requests.get(f"https://discord.com/api/v9/users/@me", headers=headers)

            servers_count = len(servers_response.json())
            friends_count = len(friends_response.json())
            badges = badges_response.json().get("flags", 0)

           
            badge_names = {
                Discord_Employee: "Discord Employee",
                Partnered_Server_Owner: "Partnered Server Owner",
                HypeSquad_Events: "HypeSquad Events",
                Bug_Hunter_Level_1: "Bug Hunter Level 1",
                House_Bravery: "House Bravery",
                House_Brilliance: "House Brilliance",
                House_Balance: "House Balance",
                Early_Supporter: "Early Supporter",
                Bug_Hunter_Level_2: "Bug Hunter Level 2",
                Early_Verified_Bot_Developer: "Early Verified Bot Developer",
                No_Badge: "No Badge"
            }

            badge_status = ", ".join(badge_names[badge] for badge in badge_names if badges & badge)

            
            guilds_with_perms = [guild["name"] for guild in servers_response.json() if guild.get("owner") or (guild.get("roles") and any(role["permissions"] & 0x8 for role in guild["roles"]))]
            guild_names = ", ".join(guilds_with_perms)

            print(f"[{time.strftime('%H:%M:%S')} Valid ({token[:32]}...)]")
            print(f"User ID: {user_id}")
            print(f"Username: {username}#{discriminator}")
            print(f"Banner URL: {banner_url}")
            print(f"Avatar URL: {avatar_url}")
            print(f"Locale: {locale}")
            print(f"NSFW Allowed: {nsfw_allowed}")
            print(f"MFA Enabled: {mfa_enabled}")
            print(f"Creation Date: {creation_date}")
            print(f"Nitro Status: {premium_type}")
            print(f"Verified: {verified}")
            print(f"Phone: {phone}")
            print(f"Email: {email}")
            print(f"Servers: {servers_count}")
            print(f"Friends: {friends_count}")
            print(f"Badges: {badge_status}")
            print(f"Server Administrator: {guild_names}")
            print("-" * 30)

            valid_tokens.append((token, user_id, username, discriminator, banner_url, avatar_url, locale, nsfw_allowed, mfa_enabled, creation_date, premium_type, verified, phone, email, servers_count, friends_count, badges))
       
            payment_url = "https://discord.com/api/users/@me/billing/payment-sources"
            payment_response = requests.get(payment_url, headers=headers)
            if payment_response.status_code in [200, 201, 204]:
                payments = []
                for data in payment_response.json():
                    if int(data['type'] == 1):
                        payments.append({'type': "Credit Card",
                                         'valid': not data['invalid'],
                                         'brand': data['brand'],
                                         'last 4': data['last_4'],
                                         'expires': str(data['expires_year']) + "y " + str(data['expires_month']) + 'm',
                                         'billing name': data['billing_address']['name'],
                                         'country': data['billing_address']['country'],
                                         'state': data['billing_address']['state'],
                                         'city': data['billing_address']['city'],
                                         'zip code': data['billing_address']['postal_code'],
                                         'address': data['billing_address']['line_1'], })
                    else:
                        payments.append({'type': "Paypal",
                                         'valid': not data['invalid'],
                                         'email': data['email'], 'billing name': data['billing_address']['name'],
                                         'country': data['billing_address']['country'],
                                         'state': data['billing_address']['state'],
                                         'city': data['billing_address']['city'],
                                         'zip code': data['billing_address']['postal_code'],
                                         'address': data['billing_address']['line_1'], })
                payment_tokens.append((token, payments))
            else:
                print(f"[{time.strftime('%H:%M:%S')} Payment Error ({token[:32]}...): {payment_response.text}")
        elif response.status_code == 401:
            invalid_tokens.append(token)
            print(f"[{time.strftime('%H:%M:%S')} Invalid ({token[:32]}...)]")
        elif response.status_code == 403:
            locked_tokens.append(token)
            print(f"[{time.strftime('%H:%M:%S')} Locked ({token[:32]}...)]")
        else:
            unknown_tokens.append(token)
            print(f"[{time.strftime('%H:%M:%S')} Unknown ({token[:32]}...)]")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')} Error ({token[:32]}...): {e}")

end_time = time.time()

print(f"\nResults:\n[-] Valid: {len(valid_tokens)}\n[-] Invalid: {len(invalid_tokens)}\n[-] Locked: {len(locked_tokens)}\n[-] Unknown: {len(unknown_tokens)}\n[-] No Nitro: {len(no_nitro_tokens)}\n[-] Nitro Classic: {len(nitro_classic_tokens)}\n[-] Nitro Boost: {len(nitro_boost_tokens)}\n[-] Verified True: {len(verified_true_tokens)}\n[-] Verified False: {len(verified_false_tokens)}\n[-] Phone True: {len(phone_true_tokens)}\n[-] Phone False: {len(phone_false_tokens)}\n[-] Time Taken: {end_time - start_time:.2f} seconds")


for token, payments in payment_tokens:
    print(f"\nPayments for Token: {token}")
    for payment in payments:
        print("Payment Type:", payment['type'])
        print("Valid:", payment['valid'])
        if payment['type'] == "Credit Card":
            print("Brand:", payment['brand'])
            print("Last 4:", payment['last 4'])
            print("Expires:", payment['expires'])
        else:
            print("Email:", payment['email'])
        print("Billing Name:", payment['billing name'])
        print("Country:", payment['country'])
        print("State:", payment['state'])
        print("City:", payment['city'])
        print("Zip Code:", payment['zip code'])
        print("Address:", payment['address'])
        print("-" * 30)
