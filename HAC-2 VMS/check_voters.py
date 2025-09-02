import sqlite3

# Connect to the database
conn = sqlite3.connect("voting.db")
cursor = conn.cursor()

# Fetch all registered voters
cursor.execute("SELECT id, name, voter_id, has_voted FROM voters")
voters = cursor.fetchall()

# Display the voters
if voters:
    print("Registered Voters:")
    print("-" * 40)
    for voter in voters:
        print(f"ID: {voter[0]}, Name: {voter[1]}, Voter ID: {voter[2]}, Has Voted: {bool(voter[3])}")
else:
    print("No registered voters found.")

# Close the connection
conn.close()
