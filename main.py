import datetime,json,requests,random
from time import sleep


def sendDiscord(webhook_url, content: dict):
    response = requests.post(webhook_url, data=json.dumps(content), headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
    })
    return response

with open("settings.json", "r") as f:
    settings = json.load(f)

def get_next_birthday(today, birthdays):
    today_date = datetime.datetime.strptime(today, "%m/%d")
    closest_date = None
    closest_character = None

    for character in birthdays:
        birthday_date = datetime.datetime.strptime(character["birthday"], "%m/%d")
        # Handle year wraparound for dates earlier in the year
        if birthday_date < today_date:
            birthday_date = birthday_date.replace(year=today_date.year + 1)
        else:
            birthday_date = birthday_date.replace(year=today_date.year)

        if closest_date is None or birthday_date < closest_date:
            closest_date = birthday_date
            closest_character = character

    return closest_character


def main(m):
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
            next_character_name = next_character["fullName"] if next_character["fullName"] else next_character["name"]
            next_birthday_date = next_character["birthday"]
            embed = {
                "username": f'{m["name"]}-{random.randint(10, 90)}',
                "avatar_url": avatar_url,
                "embeds": [
                    {
                        "title": f"🎉 Happy Birthday, {full_name if full_name else name}! 🎂",
                        "image": {"url": image_url},
                        "color": 0x38f4af,
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "footer": {"text": f"Next Birthday: {next_character_name} on {next_birthday_date}"},
                    }
                ]
            }

            response = sendDiscord(m["webhook"], embed)
            if response.ok:
                print(f"Successfully sent birthday message for {full_name if full_name else name}.")
            else:
                print(f"Failed to send birthday message for {full_name if full_name else name}: {response.status_code}, {response.text}")
            sleep(5)

main(settings)
