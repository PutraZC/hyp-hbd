import datetime
import json
import requests
import random
from time import sleep

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%m/%d")
        return True
    except ValueError:
        return False

def get_next_birthday(today, birthdays):
    today_date = datetime.datetime.strptime(today, "%m/%d")
    valid_birthdays = [
        character for character in birthdays if is_valid_date(character["birthday"])
    ]
    
    upcoming_birthdays = []
    for character in valid_birthdays:
        birthday_date = datetime.datetime.strptime(character["birthday"], "%m/%d")
        birthday_date = birthday_date.replace(year=today_date.year)
        if birthday_date < today_date:
            birthday_date = birthday_date.replace(year=today_date.year + 1)
        upcoming_birthdays.append((character, birthday_date))
    
    upcoming_birthdays.sort(key=lambda x: x[1])
    return upcoming_birthdays[0][0] if upcoming_birthdays else None

def sendDiscord(webhook_url, content: dict):
    response = requests.post(webhook_url, data=json.dumps(content), headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
    })
    return response

def main(settings):
    with open("birthdays.json", "r") as f:
        birthdays = json.load(f)

    today = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).strftime("%m/%d")
    for character in birthdays:
        if character["birthday"] == today:
            name = character["name"]
            full_name = character["fullName"]
            costume = character["costume"]
            image_url = f"https://gi.yatta.moe/assets/UI/UI_Costume_{costume}.png" if costume else f"https://gi.yatta.moe/assets/UI/UI_Gacha_AvatarImg_{name}.png"
            avatar_url = f"https://gi.yatta.moe/assets/UI/UI_AvatarIcon_{costume}.png" if costume else f"https://gi.yatta.moe/assets/UI/UI_AvatarIcon_{name}.png"

            print(f"Today: {today}, Checking: {character['birthday']}")

            next_character = get_next_birthday(today, birthdays)
            next_character_name = next_character["fullName"] or next_character["name"]
            
            embed = {
                "username": f'{settings["name"]}-{random.randint(10, 90)}',
                "avatar_url": avatar_url,
                "embeds": [
                    {
                        "title": f"🎉 Happy Birthday, {full_name or name}! 🎂",
                        "image": {"url": image_url},
                        "color": 0x38f4af,
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "footer": {"text": f"Upcoming Character: {next_character_name}"},
                    }
                ]
            }

            response = sendDiscord(settings["webhook"], embed)
            if response.ok:
                print(f"Successfully sent birthday message for {full_name or name}.")
            else:
                print(f"Failed to send birthday message for {full_name or name}: {response.status_code}, {response.text}")
            sleep(5)

with open("settings.json", "r") as f:
    settings = json.load(f)
main(settings)
