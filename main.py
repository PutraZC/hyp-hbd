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

            # Get Next upcoming character birthday
            nextBirthday = birthdays[birthdays.index(character) + 1]
            characterName = full_name if full_name else name
            embed = {
                "username": f'{m["name"]}-{random.randint(10, 90)}',
                "avatar_url": avatar_url,
                "embeds": [
                    {
                        "title": f"🎉 Happy Birthday, {characterName}! 🎂",
                        "image": {"url": image_url},
                        "color": 0x38f4af,
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "footer": {"text": f"Upcoming Character: {nextBirthday['fullName']}"}, 
                    }
                ]
            }

            response = sendDiscord(m["webhook"], embed)
            if response.ok:
                print(f"Successfully sent birthday message for {characterName}.")
            else:
                print(f"Failed to send birthday message for {characterName}: {response.status_code}, {response.text}")
            sleep(5)

main(settings)
