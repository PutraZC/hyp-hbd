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

def getNextBirthDay(current_date, birthdays):
    monthDay = (current_date.month, current_date.day)
    
    birthday_dates = []
    for character in birthdays:
        try:
            bday_str = character["birthday"]
            month, day = map(int, bday_str.split("/"))
            birthday_dates.append(((month, day), character))
        except:
            continue
    
    birthday_dates.sort(key=lambda x: x[0])
    
    for (month, day), character in birthday_dates:
        if (month, day) > monthDay:
            return character, month, day
    if birthday_dates:
        return birthday_dates[0][1], birthday_dates[0][0][0], birthday_dates[0][0][1]
    
    return None, None, None

def main(m):
    with open("birthdays.json", "r") as f:
        birthdays = json.load(f)
    
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
    today = now.strftime("%m/%d")
    
    next_char, next_month, next_day = getNextBirthDay(now, birthdays)
    
    for character in birthdays:
        if character["birthday"] == today:
            name = character["name"]
            full_name = character["fullName"]
            costume = character["costume"]
            image_url = f"https://api.hakush.in/gi/UI/UI_Costume_{costume}.webp" if costume else f"https://api.hakush.in/gi/UI/UI_Gacha_AvatarImg_{name}.webp"
            avatar_url = f"https://api.hakush.in/gi/UI/UI_AvatarIcon_{costume}.webp" if costume else f"https://api.hakush.in/gi/UI/UI_AvatarIcon_{name}.webp"

            print(f"Today: {today}, Checking: {character['birthday']}")

            characterName = full_name if full_name else name
            
            #footer_text = "@putrazc "
            
            if next_char:
                next_name = next_char["fullName"] if next_char["fullName"] else next_char["name"]
                month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                month_name = month_names[next_month - 1]
                next_bday_str = f"{next_char['birthday']} or {next_day} {month_name}"
                footer_text = f"Next Character Birthday: {next_name} on {next_bday_str}"

            embed = {
                "username": f'{m["name"]}-{random.randint(10, 90)}',
                "avatar_url": avatar_url,
                "embeds": [
                    {
                        "title": f"🎉 Happy Birthday, {characterName}! 🎂",
                        "image": {"url": image_url},
                        "color": 0x38f4af,
                        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "footer": {"text": footer_text}  
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