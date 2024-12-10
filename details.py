import csv

async def extract_details_by_email(target_email, filename="scoreboard.csv"):
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        current_place = None
        current_team_name = None
        
        for row in csv_reader:
            if row[0]:  # This row has place and team info
                current_place = row[0]
                current_team_name = row[1]
            elif current_team_name:  # This row has member info
                member_name = row[4]
                member_email = row[6]
                
                if member_email == target_email:  # Check if the email matches
                    return {
                        'place': current_place,
                        'team_name': current_team_name,
                        'member_name': member_name,
                        'member_email': member_email
                    }
    return None
    