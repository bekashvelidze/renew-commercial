import mariadb
from connection import Database

phone = "598080090"
minutes = 9

db = Database()
conn = db.connect()
cursor4 = conn.cursor()
cursor4.execute("SELECT * FROM clients WHERE phone=%s", (phone,))
# existing = []
# for client in cursor4:
#     existing.append(client[5])
existing = [minute[5] for minute in cursor4]
print(existing)
existing_minutes = existing[0]
updated_minutes = existing_minutes + int(minutes)
print(updated_minutes)
# cursor5 = conn.cursor()
# cursor5.execute(f"UPDATE clients SET 'minutes'={updated_minutes} WHERE phone=%s", (phone,))
