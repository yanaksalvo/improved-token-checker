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
            print(f"[{time.strftime('%H:%M:%S')} Valid ({token[:32]}...) - User ID: {user_id}, Username: {username}#{discriminator}, Banner URL: {banner_url}, Avatar URL: {avatar_url}, Locale: {locale}, NSFW Allowed: {nsfw_allowed}, MFA Enabled: {mfa_enabled}, Creation Date: {creation_date}, Nitro Status: {premium_type}, Verified: {verified}, Phone: {phone}, Email: {email}, Servers: {servers_count}, Friends: {friends_count}, Badges: {badge_status}")

            valid_tokens.append((token, user_id, username, discriminator, banner_url, avatar_url, locale, nsfw_allowed, mfa_enabled, creation_date, premium_type, verified, phone, email, servers_count, friends_count, badges))
        
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


with open("valid.txt", "w") as f_valid, open("no_nitro.txt", "w") as f_no_nitro, open("nitro_classic.txt", "w") as f_nitro_classic, open("nitro_boost.txt", "w") as f_nitro_boost, open("verified_true.txt", "w") as f_verified_true, open("verified_false.txt", "w") as f_verified_false, open("phone_true.txt", "w") as f_phone_true, open("phone_false.txt", "w") as f_phone_false, open("email_tokens.txt", "w") as f_email_tokens:
    for token, user_id, username, discriminator, banner_url, avatar_url, locale, nsfw_allowed, mfa_enabled, creation_date, premium_type, verified, phone, email in valid_tokens:
        f_valid.write(f"{token.strip()} - User ID: {user_id}, Username: {username}#{discriminator}, Banner URL: {banner_url}, Avatar URL: {avatar_url}, Locale: {locale}, NSFW Allowed: {nsfw_allowed}, MFA Enabled: {mfa_enabled}, Creation Date: {creation_date}, Nitro Status: {premium_type}, Verified: {verified}, Phone: {phone}, Email: {email}\n")
        if premium_type == 0:
            f_no_nitro.write(f"{token.strip()} - User ID: {user_id}, Username: {username}#{discriminator}\n")
        elif premium_type == 1:
            f_nitro_classic.write(f"{token.strip()} - User ID: {user_id}, Username: {username}#{discriminator}\n")
        elif premium_type == 2:
            f_nitro_boost.write(f"{token.strip()} - User ID: {user_id}, Username: {username}#{discriminator}\n")
        if verified:
            f_verified_true.write(f"{token.strip()} - User ID: {user_id}, Username: {username}#{discriminator}\n")
        else:
            f_verified_false.write(f"{token.strip()} - User ID: {user_id}, Username: {username}#{discriminator}\n")
        if phone:
            f_phone_true.write(f"{token.strip()} - User ID: {user_id}, Username: {username}#{discriminator}\n")
        else:
            f_phone_false.write(f"{token.strip()} - User ID: {user_id}, Username: {username}#{discriminator}\n")
        if email:
            f_email_tokens.write(f"{token.strip()} - User ID: {user_id}, Username: {username}#{discriminator}, Email: {email}\n")

with open("invalid.txt", "w") as f:
    f.writelines(invalid_tokens)

with open("locked.txt", "w") as f:
    f.writelines(locked_tokens)

with open("unknown.txt", "w") as f:
    f.writelines(unknown_tokens)
