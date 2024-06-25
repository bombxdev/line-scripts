import requests
import pandas as pd

def get_friends_from_line(token, groupId):
    url = f'https://api.line.me/v2/bot/group/{groupId}/members/ids'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    all_data = []

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching data: {response.text}")
            break

        json = response.json()
        print(f"Fetched {len(json.get('memberIds', []))} user IDs")

        user_ids = json.get('memberIds', [])
        if not user_ids:
            break

        for user_id in user_ids:
            profile_url = f'https://api.line.me/v2/bot/profile/{user_id}'
            profile_response = requests.get(profile_url, headers=headers)
            if profile_response.status_code == 200:
                profile = profile_response.json()
                all_data.append([
                    profile.get('userId', ''),
                    profile.get('displayName', ''),
                    profile.get('pictureUrl', ''),
                    profile.get('statusMessage', '')
                ])

        if 'next' in json:
            url = f'https://api.line.me/v2/bot/group/{groupId}/members/ids?start={json["next"]}'
        else:
            break

    return all_data

def export_to_excel(data):
    df = pd.DataFrame(data, columns=['UserID', 'DisplayName', 'PictureURL', 'StatusMessage'])
    df.to_excel('line_members_in_group.xlsx', index=False)
    print("Data exported to line_members_in_group.xlsx")

def main():
    token = input("Enter your Channel Access Token: ")
    groupId = input("Enter your groupId: ")
    friends_data = get_friends_from_line(token, groupId)
    if friends_data:
        export_to_excel(friends_data)
    else:
        print("No data to export")

if __name__ == "__main__":
    main()
