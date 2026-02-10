
import MySQLdb

try:
    db = MySQLdb.connect(
        host="127.0.0.1",
        user="rhms_user",
        passwd="klsaDb23@#",
        db="reevanahms"
    )

    cursor = db.cursor()
    cursor.execute("SELECT email FROM accounts_user WHERE is_superuser = 1")
    results = cursor.fetchall()

    if results:
        print("Superusers found:")
        for (email,) in results:
            print(f"Email: {email}")
    else:
        print("No superusers found.")

    db.close()

except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")
