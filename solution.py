import traceback
import requests

url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"

user_details = {
    "name": "Shriyash Beohar",
    "email": "shriyashbeohar221179@acropolis.in",
    "regNo": "0827CI221127" 
}

print("Sending POST request to fetch webhook and access token...")
register_response = requests.post(url, json=user_details)
register_data = register_response.json()

print("Response received:", register_data)


webhook_url = register_data.get("webhook")
access_token = register_data.get("accessToken")

if not webhook_url or not access_token:
    print("Error: Failed to retrieve webhook or access token.", traceback.format_exc())
    exit()


#PostgreSQL query
final_sql_query = """
SELECT 
    e.FIRST_NAME || ' ' || e.LAST_NAME AS NAME,
    FLOOR(EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.DOB))) AS AGE,
    d.DEPARTMENT_NAME,
    p.AMOUNT AS SALARY
FROM 
    PAYMENTS p
JOIN 
    EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN 
    DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE 
    EXTRACT(DAY FROM p.PAYMENT_TIME) != 1
    AND p.AMOUNT = (
        SELECT MAX(AMOUNT)
        FROM PAYMENTS
        WHERE EXTRACT(DAY FROM PAYMENT_TIME) !=1
    );
"""


headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

submit_data = {
    "finalQuery": final_sql_query.strip()
}

print("Submitting final SQL query...")
submit = requests.post(webhook_url, headers=headers, json=submit_data)


print("Status:", submit.status_code)
print("Response:", submit.json())
