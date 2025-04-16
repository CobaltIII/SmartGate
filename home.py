# '''import streamlit as st
# from datetime import datetime
# import asyncio
# import asyncpg
# import os
# from dotenv import load_dotenv
# import nest_asyncio 
# import random
# import string
# import time
# from datetime import datetime
# import pandas as pd

# nest_asyncio.apply()
# load_dotenv()

# DB_URL = os.getenv("URI")
# db_pool = None

# if "activity_log" not in st.session_state:
#     st.session_state.activity_log = [
#         "You logged in!"
#     ]


# async def connect_to_db():
#     global db_pool
#     if not db_pool:
#         db_pool = await asyncpg.create_pool(dsn=DB_URL)

# async def disconnect_from_db():
#     global db_pool
#     if db_pool:
#         await db_pool.close()

# async def get_connection():
#     global db_pool
#     return await db_pool.acquire()

# async def get_service_orders(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT S.Service_Name, R.Order_ID, R.Date, R.Time, R.Delivery_Status
#             FROM Resident_Orders_Service R
#             JOIN Services S ON R.Service_ID = S.Service_ID
#             WHERE R.House_Number = $1
#             ORDER BY R.Date DESC, R.Time DESC
#         """, house_number)
#         return rows
# async def get_all_amenities():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Amenity_ID, Amenity_Name, Availability_Status, Operating_Hours
#             FROM Amenities
#             ORDER BY Amenity_Name
#         """)
#         return rows
# async def get_all_services():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Service_ID, Service_Name, Provider_Name, Cost
#             FROM Services
#             ORDER BY Service_Name
#         """)
#         return rows

# def generate_passkey():
#     digits = ''.join(random.choices(string.digits, k=6))
#     return digits

# async def get_visitors(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Visitor_Name, Visit_Purpose,phone_number
#             FROM Visitor
#             ORDER BY Visitor_Name
#         """)
#         return rows

# def add_log(message):
#     timestamp = datetime.now().strftime("%I:%M %p")
#     st.session_state.activity_log.insert(0, f"{timestamp} {message}")

# async def get_activity_log():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Activity_Description, Timestamp
#             FROM Activity_Log
#             WHERE House_Number = $1
#             ORDER BY Timestamp DESC
#         """, house_number)
#         return rows

# async def get_cars(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT registration_number,model, parking_spot_number
#             FROM Car
#             WHERE resident_house_number = $1
#         """, house_number)
#         return rows

# async def get_booked_amenities(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#         SELECT A.Amenity_Name, R.Booking_Date, R.Start_Time, R.End_Time, R.Number_of_people
#         FROM Resident_Books_Amenity R
#         JOIN Amenities A ON A.Amenity_ID = R.Amenity_ID
#         WHERE R.House_Number = $1
#     """, house_number)
#         return rows


# # Run once when app starts
# asyncio.run(connect_to_db())

# # --- PAGE CONFIG ---
# st.set_page_config(page_title="SmartGate Dashboard", layout="wide")

# # --- HEADER ---
# with st.container():
#     cols = st.columns([2, 8, 2])
#     with cols[0]:
#         st.markdown("### SmartGate")
#     with cols[1]:
#         st.markdown(f"{datetime(2024, 4, 24, 12, 0).strftime('%B %d, %Y %I:%M %p')}")
#     with cols[2]:
#         st.image("https://randomuser.me/api/portraits/women/44.jpg", width=40)
#         st.markdown("*Esther Howard*")

# st.markdown("---")

# # --- SIDEBAR ---
# with st.sidebar:
#     st.markdown("## 📋 Dashboard")
#     st.button("🏠 Dashboard")
#     st.button("🧑‍🤝‍🧑 My Visitors")
#     st.button("📅 Book Amenity")
#     st.button("🛠 Order Services")
#     st.button("🚗 My Cars")

# # --- MAIN DASHBOARD HEADER ---
# st.markdown("## Hi, Esther Howard\nWelcome back!")
# st.markdown("Here's a quick overview of your society activities.")

# # --- MAIN GRID ---
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("### Add Visitor")
#     visitor_name = st.text_input("Visitor Name")
#     visit_date = st.date_input("Date of Visit")
#     purpose = st.text_input("Purpose")
#     st.text_input("Passkey", value=str(generate_passkey()), disabled=True)

#     if st.button("Submit") and visitor_name and purpose:
#         full_visit_time = visit_date
#         visit_id = (
#             full_visit_time.year
#             + full_visit_time.month
#             + full_visit_time.day
#         )

#         async def add_visitor():
#             async with db_pool.acquire() as conn:
#                 await conn.execute("""
#                     INSERT INTO Visitor (Visitor_ID, Visitor_Name, Phone_Number, Has_Passkey, Visit_Purpose)
#                     VALUES ($1, $2, $3, $4, $5)
#                 """, visit_id, visitor_name, "9876543210", True, purpose)

#         asyncio.get_event_loop().run_until_complete(add_visitor())
#         add_log(f"Visitor added: *{visitor_name}*")
#         st.success("Visitor added to the system.")

#     bookings = asyncio.get_event_loop().run_until_complete(get_booked_amenities(house_number))

#     if bookings:
#         df_amenities = pd.DataFrame([dict(row) for row in bookings])
#         df_amenities.columns = ["Amenity", "Date", "Start", "End", "People"]
        
#         st.markdown("### Booked Amenities")
#         st.table(df_amenities)
#     st.markdown("### ➕ Book a New Amenity")

#     amenities = asyncio.get_event_loop().run_until_complete(get_all_amenities())

#     if amenities:
#         amenity_options = [f"{row['amenity_name']} ({row['availability_status']})" for row in amenities]
#         selected = st.selectbox("Select Amenity", amenity_options, key="amenity_select")
#         selected_amenity = amenities[amenity_options.index(selected)]

#         booking_date = st.date_input("Booking Date", datetime.now().date(), key="amenity_date")
#         start_time = st.time_input("Start Time", datetime.strptime("10:00", "%H:%M").time(), key="amenity_start")
#         end_time = st.time_input("End Time", datetime.strptime("11:00", "%H:%M").time(), key="amenity_end")
#         num_people = st.number_input("Number of People", min_value=1, max_value=20, value=1, key="amenity_people")

#         if st.button("Book Amenity"):
#             booking_id = int(time.time())

#             async def book_amenity():
#                 async with db_pool.acquire() as conn:
#                     await conn.execute("""
#                         INSERT INTO Resident_Books_Amenity (
#                             House_Number, Amenity_ID, Booking_ID, Booking_Date, Start_Time, End_Time, Number_of_people
#                         ) VALUES ($1, $2, $3, $4, $5, $6, $7)
#                     """, house_number, selected_amenity["amenity_id"], booking_id, booking_date, start_time, end_time, num_people)

#             asyncio.run(book_amenity())
#             add_log(f"Booked amenity: *{selected_amenity['amenity_name']}* on {booking_date}")
#             st.success("Amenity booked successfully!")
#     else:
#         st.warning("No amenities available.")


#     st.markdown("### My Cars")

#     cars = asyncio.get_event_loop().run_until_complete(get_cars(house_number))

#     if cars:
#         df_cars = pd.DataFrame([dict(row) for row in cars])
#         df_cars.columns = ["Registration Number", "Model", "Parking Spot"]
#         st.table(df_cars)   
#     else:
#         st.info("No cars registered.")

# with col2:
#     st.markdown("### My Visitors")
#     visitors = asyncio.get_event_loop().run_until_complete(get_visitors(house_number))
#     df_visitors = pd.DataFrame(visitors)
#     df_visitors.columns = ["Visitor Name", "Visit Purpose", "Phone Number"]

#     st.markdown("### My Visitors")
#     st.table(df_visitors)  # Automatically removes index styling

#     st.markdown("### Service Orders")

#     orders = asyncio.get_event_loop().run_until_complete(get_service_orders(house_number))

#     if orders:
#         order_data = [{
#             "Order ID": row["order_id"],
#             "Service": row["service_name"],
#             "Date": row["date"].strftime("%b %d, %Y"),
#             "Time": row["time"].strftime("%I:%M %p"),
#             "Status": row["delivery_status"]
#         } for row in orders]
#         st.table(order_data)
#     else:
#         st.info("No service orders found.")
    
#     st.markdown("### 📦 Order a Service")

#     services = asyncio.get_event_loop().run_until_complete(get_all_services())

#     if services:
#      service_names = [f"{row['service_name']} (by {row['provider_name']} - ₹{row['cost']})" for row in services]
#      selected = st.selectbox("Select Service", service_names)
#      selected_service = services[service_names.index(selected)]
    
#      order_date = st.date_input("Order Date", datetime.now().date())
#      order_time = st.time_input("Order Time", datetime.now().time())

#      if st.button("Place Order"):
#         order_id = int(time.time())  # Using Unix timestamp as unique Order_ID
#         async def place_order():
#             async with db_pool.acquire() as conn:
#                 await conn.execute("""
#                     INSERT INTO Resident_Orders_Service (House_Number, Service_ID, Order_ID, Date, Time, Delivery_Status)
#                     VALUES ($1, $2, $3, $4, $5, $6)
#                 """, house_number, selected_service["service_id"], order_id, order_date, order_time, "Pending")

#         asyncio.get_event_loop().run_until_complete(place_order())
#         add_log(f"Ordered service: *{selected_service['service_name']}*")
#         st.success("Service ordered successfully!")
#     else:
#      st.warning("No services available.")

#     st.markdown("### Activity Log")
#     for log_entry in st.session_state.activity_log:
#         st.markdown(f"- {log_entry}")

    
# '''



# import streamlit as st
# from datetime import datetime
# import asyncio
# import asyncpg
# import os
# from dotenv import load_dotenv
# import nest_asyncio
# import random
# import string
# import time
# import pandas as pd

# nest_asyncio.apply()
# load_dotenv()

# DB_URL = os.getenv("URI")
# db_pool = None

# if "activity_log" not in st.session_state:
#     st.session_state.activity_log = ["You logged in!"]

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.user_type = None
#     st.session_state.user_id = None

# async def connect_to_db():
#     global db_pool
#     if not db_pool:
#         db_pool = await asyncpg.create_pool(dsn=DB_URL)

# async def disconnect_from_db():
#     global db_pool
#     if db_pool:
#         await db_pool.close()

# async def get_connection():
#     global db_pool
#     return await db_pool.acquire()

# async def is_valid_resident(house_number):
#     async with db_pool.acquire() as conn:
#         result = await conn.fetchval("SELECT COUNT(*) FROM Resident WHERE House_Number = $1", house_number)
#         return result > 0

# async def is_valid_guard(badge_number):
#     async with db_pool.acquire() as conn:
#         result = await conn.fetchval("SELECT COUNT(*) FROM Guard WHERE Badge_Number = $1", badge_number)
#         return result > 0

# async def get_service_orders(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT S.Service_Name, R.Order_ID, R.Date, R.Time, R.Delivery_Status
#             FROM Resident_Orders_Service R
#             JOIN Services S ON R.Service_ID = S.Service_ID
#             WHERE R.House_Number = $1
#             ORDER BY R.Date DESC, R.Time DESC
#         """, house_number)
#         return rows

# async def get_all_amenities():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Amenity_ID, Amenity_Name, Availability_Status, Operating_Hours
#             FROM Amenities
#             ORDER BY Amenity_Name
#         """)
#         return rows

# async def get_all_services():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Service_ID, Service_Name, Provider_Name, Cost
#             FROM Services
#             ORDER BY Service_Name
#         """)
#         return rows

# def generate_passkey():
#     digits = ''.join(random.choices(string.digits, k=6))
#     return digits

# async def get_visitors():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Visitor_Name, Visit_Purpose, phone_number
#             FROM Visitor
#             ORDER BY Visitor_Name
#         """)
#         return rows

# def add_log(message):
#     timestamp = datetime.now().strftime("%I:%M %p")
#     st.session_state.activity_log.insert(0, f"{timestamp} {message}")

# async def get_activity_log(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Activity_Description, Timestamp
#             FROM Activity_Log
#             WHERE House_Number = $1
#             ORDER BY Timestamp DESC
#         """, house_number)
#         return rows

# async def get_cars(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT registration_number, model, parking_spot_number
#             FROM Car
#             WHERE resident_house_number = $1
#         """, house_number)
#         return rows

# async def get_booked_amenities(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT A.Amenity_Name, R.Booking_Date, R.Start_Time, R.End_Time, R.Number_of_people
#             FROM Resident_Books_Amenity R
#             JOIN Amenities A ON A.Amenity_ID = R.Amenity_ID
#             WHERE R.House_Number = $1
#         """, house_number)
#         return rows

# asyncio.run(connect_to_db())
# st.set_page_config(page_title="SmartGate Dashboard", layout="wide")

# if not st.session_state.logged_in:
#     st.title("🔐 Login to SmartGate")

#     user_type = st.selectbox("Login as", ["Resident", "Guard"])
#     user_id = st.text_input("Enter House Number" if user_type == "Resident" else "Enter Badge Number")
#     password = st.text_input("Enter Password", type="password")

#     if st.button("Login"):
#         if password != "1234":
#             st.error("Incorrect password.")
#         elif not user_id.strip().isdigit():
#             st.error("Please enter a valid numeric ID.")
#         else:
#             user_id = int(user_id.strip())
#             if user_type == "Resident":
#                 if asyncio.run(is_valid_resident(user_id)):
#                     st.session_state.logged_in = True
#                     st.session_state.user_type = "Resident"
#                     st.session_state.user_id = user_id
#                     st.success("Resident login successful.")
#                     st.rerun()

#                 else:
#                     st.error("House number not found.")
#             else:
#                 if asyncio.run(is_valid_guard(user_id)):
#                     st.session_state.logged_in = True
#                     st.session_state.user_type = "Guard"
#                     st.session_state.user_id = user_id
#                     st.success("Guard login successful.")
#                     st.rerun()

#                 else:
#                     st.error("Badge number not found.")
#     st.stop()

# # Place the rest of your dashboard code here

# user_id = st.session_state.user_id

# # --- HEADER ---
# with st.container():
#     cols = st.columns([2, 8, 2])
#     with cols[0]:
#         st.markdown("### SmartGate")
#     with cols[1]:
#         st.markdown(f"{datetime.now().strftime('%B %d, %Y %I:%M %p')}")
#     with cols[2]:
#         st.image("https://randomuser.me/api/portraits/women/44.jpg", width=40)
#         st.markdown(f"{st.session_state.user_type} {user_id}")

# st.markdown("---")

# # --- SIDEBAR ---
# with st.sidebar:
#     st.markdown("## 📋 Dashboard")
#     st.button("🏠 Dashboard")
#     st.button("🧑‍🤝‍🧑 My Visitors")
#     st.button("📅 Book Amenity")
#     st.button("🛠 Order Services")
#     st.button("🚗 My Cars")

# # --- MAIN DASHBOARD HEADER ---
# st.markdown(f"## Hi, {st.session_state.user_type} {user_id}Welcome back!")
# st.markdown("Here's a quick overview of your society activities.")

# # --- MAIN GRID ---
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("### Add Visitor")
#     visitor_name = st.text_input("Visitor Name")
#     visit_date = st.date_input("Date of Visit")
#     purpose = st.text_input("Purpose")
#     st.text_input("Passkey", value=str(generate_passkey()), disabled=True)

#     if st.button("Submit") and visitor_name and purpose:
#         full_visit_time = visit_date
#         visit_id = full_visit_time.year + full_visit_time.month + full_visit_time.day

#         async def add_visitor():
#             async with db_pool.acquire() as conn:
#                 await conn.execute("""
#                     INSERT INTO Visitor (Visitor_ID, Visitor_Name, Phone_Number, Has_Passkey, Visit_Purpose)
#                     VALUES ($1, $2, $3, $4, $5)
#                 """, visit_id, visitor_name, "9876543210", True, purpose)

#         asyncio.run(add_visitor())
#         add_log(f"Visitor added: *{visitor_name}*")
#         st.success("Visitor added to the system.")

#     bookings = asyncio.run(get_booked_amenities(user_id))
#     if bookings:
#         df_amenities = pd.DataFrame([dict(row) for row in bookings])
#         df_amenities.columns = ["Amenity", "Date", "Start", "End", "People"]
#         st.markdown("### Booked Amenities")
#         st.table(df_amenities)

#     st.markdown("### ➕ Book a New Amenity")
#     amenities = asyncio.run(get_all_amenities())
#     if amenities:
#         amenity_options = [f"{row['amenity_name']} ({row['availability_status']})" for row in amenities]
#         selected = st.selectbox("Select Amenity", amenity_options, key="amenity_select")
#         selected_amenity = amenities[amenity_options.index(selected)]

#         booking_date = st.date_input("Booking Date", datetime.now().date(), key="amenity_date")
#         start_time = st.time_input("Start Time", datetime.strptime("10:00", "%H:%M").time(), key="amenity_start")
#         end_time = st.time_input("End Time", datetime.strptime("11:00", "%H:%M").time(), key="amenity_end")
#         num_people = st.number_input("Number of People", min_value=1, max_value=20, value=1, key="amenity_people")

#         if st.button("Book Amenity"):
#             booking_id = int(time.time())
#             async def book_amenity():
#                 async with db_pool.acquire() as conn:
#                     await conn.execute("""
#                         INSERT INTO Resident_Books_Amenity (
#                             House_Number, Amenity_ID, Booking_ID, Booking_Date, Start_Time, End_Time, Number_of_people
#                         ) VALUES ($1, $2, $3, $4, $5, $6, $7)
#                     """, user_id, selected_amenity["amenity_id"], booking_id, booking_date, start_time, end_time, num_people)
#             asyncio.run(book_amenity())
#             add_log(f"Booked amenity: *{selected_amenity['amenity_name']}* on {booking_date}")
#             st.success("Amenity booked successfully!")
#     else:
#         st.warning("No amenities available.")

#     st.markdown("### My Cars")
#     cars = asyncio.run(get_cars(user_id))
#     if cars:
#         df_cars = pd.DataFrame([dict(row) for row in cars])
#         df_cars.columns = ["Registration Number", "Model", "Parking Spot"]
#         st.table(df_cars)
#     else:
#         st.info("No cars registered.")

# with col2:
#     st.markdown("### My Visitors")
#     visitors = asyncio.run(get_visitors(house_number))
#     df_visitors = pd.DataFrame(visitors)
#     df_visitors.columns = ["Visitor Name", "Visit Purpose", "Phone Number"]
#     st.table(df_visitors)

#     st.markdown("### Service Orders")
#     orders = asyncio.run(get_service_orders(user_id))
#     if orders:
#         order_data = [{
#             "Order ID": row["order_id"],
#             "Service": row["service_name"],
#             "Date": row["date"].strftime("%b %d, %Y"),
#             "Time": row["time"].strftime("%I:%M %p"),
#             "Status": row["delivery_status"]
#         } for row in orders]
#         st.table(order_data)
#     else:
#         st.info("No service orders found.")

#     st.markdown("### 📦 Order a Service")
#     services = asyncio.run(get_all_services())
#     if services:
#         service_names = [f"{row['service_name']} (by {row['provider_name']} - ₹{row['cost']})" for row in services]
#         selected = st.selectbox("Select Service", service_names)
#         selected_service = services[service_names.index(selected)]

#         order_date = st.date_input("Order Date", datetime.now().date())
#         order_time = st.time_input("Order Time", datetime.now().time())

#         if st.button("Place Order"):
#             order_id = int(time.time())
#             async def place_order():
#                 async with db_pool.acquire() as conn:
#                     await conn.execute("""
#                         INSERT INTO Resident_Orders_Service (House_Number, Service_ID, Order_ID, Date, Time, Delivery_Status)
#                         VALUES ($1, $2, $3, $4, $5, $6)
#                     """, user_id, selected_service["service_id"], order_id, order_date, order_time, "Pending")
#             asyncio.run(place_order())
#             add_log(f"Ordered service: *{selected_service['service_name']}*")
#             st.success("Service ordered successfully!")
#     else:
#         st.warning("No services available.")

#     st.markdown("### Activity Log")
#     for log_entry in st.session_state.activity_log:
#         st.markdown(f"- {log_entry}")

import streamlit as st
from datetime import datetime
import asyncio
import asyncpg
import os
from dotenv import load_dotenv
import nest_asyncio
import random
import string
import time
import pandas as pd
import random
from datetime import datetime

nest_asyncio.apply()
load_dotenv()

house_number = 3001
DB_URL = os.getenv("URI")
db_pool = None

query_params = st.query_params
params = st.query_params
page = query_params.get("page", "login")

if "activity_log" not in st.session_state:
    st.session_state.activity_log = ["You logged in!"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_id = None

async def connect_to_db():
    global db_pool
    if not db_pool:
        db_pool = await asyncpg.create_pool(dsn=DB_URL,min_size = 1,max_size = 1)

async def disconnect_from_db():
    global db_pool
    if db_pool:
        await db_pool.close()

async def get_connection():
    global db_pool
    return await db_pool.acquire()

async def is_valid_resident(house_number):
    async with db_pool.acquire() as conn:
        result = await conn.fetchval("SELECT COUNT(*) FROM Resident WHERE House_Number = $1", house_number)
        return result > 0

async def is_valid_guard(badge_number):
    async with db_pool.acquire() as conn:
        result = await conn.fetchval("SELECT COUNT(*) FROM Guard WHERE Badge_Number = $1", badge_number)
        return result > 0

async def get_service_orders(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT S.Service_Name, R.Order_ID, R.Date, R.Time, R.Delivery_Status
            FROM Resident_Orders_Service R
            JOIN Services S ON R.Service_ID = S.Service_ID
            WHERE R.House_Number = $1
            ORDER BY R.Date DESC, R.Time DESC
        """, house_number)
        return rows

async def get_all_amenities():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT Amenity_ID, Amenity_Name, Availability_Status, Operating_Hours
            FROM Amenities
            ORDER BY Amenity_Name
        """)
        return rows

async def get_all_services():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT Service_ID, Service_Name, Provider_Name, Cost
            FROM Services
            ORDER BY Service_Name
        """)
        return rows

def generate_passkey():
    digits = ''.join(random.choices(string.digits, k=6))
    return digits

async def get_visitors(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT V.visitor_name, V.visit_purpose, V.phone_number
            FROM Visitor V
            JOIN Permissions P ON V.Visitor_ID = P.Visitor_ID
            WHERE P.Resident_House_Number = $1;
        """,house_number)
        return rows

def add_log(message):
    timestamp = datetime.now().strftime("%I:%M %p")
    st.session_state.activity_log.insert(0, f"{timestamp} {message}")

async def get_activity_log(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT Activity_Description, Timestamp
            FROM Activity_Log
            WHERE House_Number = $1
            ORDER BY Timestamp DESC
        """, house_number)
        return rows

async def get_cars(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT registration_number, model, parking_spot_number
            FROM Car
            WHERE resident_house_number = $1
        """, house_number)
        return rows

async def get_booked_amenities(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT A.Amenity_Name, R.Booking_Date, R.Start_Time, R.End_Time, R.Number_of_people
            FROM Resident_Books_Amenity R
            JOIN Amenities A ON A.Amenity_ID = R.Amenity_ID
            WHERE R.House_Number = $1
        """, house_number)
        return rows


async def generate_unique_permission_id(conn):
    while True:
        pid = random.randint(100000, 999999)  # or any suitable range
        exists = await conn.fetchval("SELECT 1 FROM Permissions WHERE Permission_ID = $1", pid)
        if not exists:
            return pid

# Connect to the database
asyncio.run(connect_to_db())
st.set_page_config(page_title="SmartGate Dashboard", layout="wide")

def resident_dashboard():
    from datetime import datetime
    import pandas as pd
    import asyncio
    import time

    user_id = st.session_state.user_id

    if "resident_section" not in st.session_state:
        st.session_state.resident_section = "dashboard"

    # HEADER
    with st.container():
        cols = st.columns([2, 8, 2])
        with cols[0]:
            st.markdown("### SmartGate")
        with cols[1]:
            st.markdown(f"{datetime.now().strftime('%B %d, %Y %I:%M %p')}")
        with cols[2]:
            st.image("https://randomuser.me/api/portraits/women/44.jpg", width=40)
            st.markdown(f"{st.session_state.user_type} {user_id}")

    st.markdown("---")

    # SIDEBAR
    with st.sidebar:
        st.markdown("## 📋 Dashboard")
        if st.button("🏠 Dashboard"):
            st.session_state.resident_section = "dashboard"
        if st.button("🧑‍🤝‍🧑 My Visitors"):
            st.session_state.resident_section = "visitors"
        if st.button("📅 Book Amenity"):
            st.session_state.resident_section = "book_amenity"
        if st.button("🛠 Order Services"):
            st.session_state.resident_section = "services"
        if st.button("🚗 My Cars"):
            st.session_state.resident_section = "cars"
        st.markdown("---")
        if st.button("🔓 Logout"):
            for key in ["logged_in", "user_type", "user_id", "activity_log", "resident_section"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # MAIN BODY CONTENT
    section = st.session_state.resident_section
    house_number = user_id  # Assuming user_id maps to house number

    if section == "dashboard":
        st.markdown(f"## Hi, {st.session_state.user_type} {user_id} — Welcome back!")
        st.markdown("Here's a quick overview of your society activities.")

        async def fetch_stats(house_number):
            async with db_pool.acquire() as conn:
                visitors = await conn.fetchval("""
                    SELECT COUNT(*) FROM Permissions WHERE Resident_House_Number = $1
                """, house_number)

                cars = await conn.fetchval("""
                    SELECT COUNT(*) FROM Car WHERE Resident_House_Number = $1
                """, house_number)

                amenities = await conn.fetchval("""
                    SELECT COUNT(*) FROM Resident_Books_Amenity WHERE House_Number = $1
                """, house_number)

                services = await conn.fetchval("""
                    SELECT COUNT(*) FROM Resident_Orders_Service WHERE House_Number = $1
                """, house_number)

                return {
                    "Visitors Approved": visitors or 0,
                    "Cars Registered": cars or 0,
                    "Amenities Booked": amenities or 0,
                    "Services Ordered": services or 0
                }

        stats = asyncio.run(fetch_stats(user_id))

        col1, col2 = st.columns(2)
        with col1:
            st.metric("👥 Visitors Approved", stats["Visitors Approved"])
            st.metric("🚗 Cars Registered", stats["Cars Registered"])
        with col2:
            st.metric("🏓 Amenities Booked", stats["Amenities Booked"])
            st.metric("🧹 Services Ordered", stats["Services Ordered"])

    elif section == "visitors":
        st.markdown("## 🧑‍🤝‍🧑 My Visitors")

        async def get_my_visitors(house_number):
            async with db_pool.acquire() as conn:
                return await conn.fetch("""
                    SELECT v.Visitor_ID, v.Visitor_Name, v.Phone_Number, v.Has_Passkey, v.Visit_Purpose
                    FROM Permissions p
                    JOIN Visitor v ON p.Visitor_ID = v.Visitor_ID
                    WHERE p.Resident_House_Number = $1
                """, house_number)

        async def approve_passkey(visitor_id):
            async with db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE Visitor
                    SET Has_Passkey = TRUE
                    WHERE Visitor_ID = $1
                """, visitor_id)

        visitors = asyncio.run(get_my_visitors(house_number))
        search = st.text_input("🔍 Search Visitor by Name or Phone")

        pending_visitors = [v for v in visitors if not v['has_passkey'] and (search.lower() in v['visitor_name'].lower() or search in v['phone_number'])]
        approved_visitors = [v for v in visitors if v['has_passkey'] and (search.lower() in v['visitor_name'].lower() or search in v['phone_number'])]

        if pending_visitors:
            st.markdown("### ⏳ Visitors Pending Approval")
            for v in pending_visitors:
                with st.container():
                    st.markdown(f"**{v['visitor_name']}** - {v['phone_number']} ({v['visit_purpose']})")
                    if st.button(f"✅ Approve {v['visitor_name']}", key=f"approve_{v['visitor_id']}"):
                        asyncio.run(approve_passkey(v['visitor_id']))
                        st.success(f"{v['visitor_name']} approved successfully!")
                        add_log(f"{v['visitor_name']} approved for entry")
                        st.rerun()


        st.markdown("### ✅ Approved Visitors")
        if approved_visitors:
            df_approved = pd.DataFrame([{
                "Name": v['visitor_name'],
                "Phone": v['phone_number'],
                "Purpose": v['visit_purpose']
            } for v in approved_visitors])
            st.table(df_approved)
        else:
            st.info("No approved visitors found.")

        # Add Visitor Section
        st.markdown("---")
        st.markdown("### ➕ Add Visitor")
        visitor_name = st.text_input("Visitor Name")
        visit_date = st.date_input("Date of Visit")
        purpose = st.text_input("Purpose")
        st.text_input("Passkey", value=str(generate_passkey()), disabled=True)

        if st.button("Submit") and visitor_name and purpose:
            full_visit_time = visit_date
            visit_id = full_visit_time.year + full_visit_time.month + full_visit_time.day

            async def add_visitor():
                async with db_pool.acquire() as conn:
                    async with conn.transaction():
                        permission_id = await generate_unique_permission_id(conn)

                        await conn.execute("""
                            INSERT INTO Visitor (Visitor_ID, Visitor_Name, Phone_Number, Has_Passkey, Visit_Purpose)
                            VALUES ($1, $2, $3, $4, $5)
                        """, visit_id, visitor_name, "9876543210", True, purpose)

                        await conn.execute("""
                            INSERT INTO Permissions (Permission_ID, Issue_Time, Approval_Status, Resident_House_Number, Visitor_ID, Guard_Badge_Number)
                            VALUES ($1, $2, $3, $4, $5, $6)
                        """, permission_id, datetime.now(), True, house_number, visit_id, 1001)

                        await conn.execute("""
                            INSERT INTO Permission_Asked_From_Resident (Permission_ID, House_Number)
                            VALUES ($1, $2)
                        """, permission_id, house_number)

                        await conn.execute("""
                            INSERT INTO Permission_Asked_For_Visitor (Permission_ID, Visitor_ID)
                            VALUES ($1, $2)
                        """, permission_id, visit_id)

            asyncio.run(add_visitor())
            add_log(f"Visitor added: **{visitor_name}**")
            st.success("Visitor added to the system.")

    elif section == "book_amenity":
        bookings = asyncio.run(get_booked_amenities(user_id))
        if bookings:
            df_amenities = pd.DataFrame([dict(row) for row in bookings])
            df_amenities.columns = ["Amenity", "Date", "Start", "End", "People"]
            st.markdown("### Booked Amenities")
            st.table(df_amenities)

        st.markdown("### ➕ Book a New Amenity")
        amenities = asyncio.run(get_all_amenities())
        if amenities:
            amenity_options = [f"{row['amenity_name']} ({row['availability_status']})" for row in amenities]
            selected = st.selectbox("Select Amenity", amenity_options, key="amenity_select")
            selected_amenity = amenities[amenity_options.index(selected)]

            booking_date = st.date_input("Booking Date", datetime.now().date(), key="amenity_date")
            start_time = st.time_input("Start Time", datetime.strptime("10:00", "%H:%M").time(), key="amenity_start")
            end_time = st.time_input("End Time", datetime.strptime("11:00", "%H:%M").time(), key="amenity_end")
            num_people = st.number_input("Number of People", min_value=1, max_value=20, value=1, key="amenity_people")

            if st.button("Book Amenity"):
                booking_id = int(time.time())

                async def book_amenity():
                    async with db_pool.acquire() as conn:
                        await conn.execute("""
                            INSERT INTO Resident_Books_Amenity (
                                House_Number, Amenity_ID, Booking_ID, Booking_Date, Start_Time, End_Time, Number_of_people
                            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                        """, user_id, selected_amenity["amenity_id"], booking_id, booking_date, start_time, end_time, num_people)

                asyncio.run(book_amenity())
                add_log(f"Booked amenity: *{selected_amenity['amenity_name']}* on {booking_date}")
                st.success("Amenity booked successfully!")
        else:
            st.warning("No amenities available.")

    elif section == "services":
        st.markdown("### Service Orders")
        orders = asyncio.run(get_service_orders(user_id))
        if orders:
            order_data = [{
                "Order ID": row["order_id"],
                "Service": row["service_name"],
                "Date": row["date"].strftime("%b %d, %Y"),
                "Time": row["time"].strftime("%I:%M %p"),
                "Status": row["delivery_status"]
            } for row in orders]
            st.table(order_data)
        else:
            st.info("No service orders found.")

        st.markdown("### 📦 Order a Service")
        services = asyncio.run(get_all_services())
        if services:
            service_names = [f"{row['service_name']} (by {row['provider_name']} - ₹{row['cost']})" for row in services]
            selected = st.selectbox("Select Service", service_names)
            selected_service = services[service_names.index(selected)]

            order_date = st.date_input("Order Date", datetime.now().date())
            order_time = st.time_input("Order Time", datetime.now().time())

            if st.button("Place Order"):
                order_id = int(time.time())

                async def place_order():
                    async with db_pool.acquire() as conn:
                        await conn.execute("""
                            INSERT INTO Resident_Orders_Service (House_Number, Service_ID, Order_ID, Date, Time, Delivery_Status)
                            VALUES ($1, $2, $3, $4, $5, $6)
                        """, user_id, selected_service["service_id"], order_id, order_date, order_time, "Pending")
                        add_log(f"Ordered service: *{selected_service['service_name']}*")

                asyncio.run(place_order())
                st.success("Service ordered successfully!")
        else:
            st.warning("No services available.")

    elif section == "cars":
        st.markdown("### My Cars")
        cars = asyncio.run(get_cars(user_id))
        if cars:
            df_cars = pd.DataFrame([dict(row) for row in cars])
            df_cars.columns = ["Registration Number", "Model", "Parking Spot"]
            st.table(df_cars)
        else:
            st.info("No cars registered.")

    # Activity Log (optional in all views)
    st.markdown("---")
    st.markdown("### Activity Log")
    for log_entry in st.session_state.activity_log:
        st.markdown(f"- {log_entry}")
def guard_dashboard():
    async def get_guard_info(badge_number):
        async with db_pool.acquire() as conn:
            return await conn.fetchrow("""
                SELECT Shift_Timings, Date_Of_Joining
                FROM Guard
                WHERE Badge_Number = $1
            """, badge_number)

    async def get_visitorsGuard():
        async with db_pool.acquire() as conn:
            return await conn.fetch("""
                SELECT v.*
                FROM Visitor v
                JOIN Permissions p ON v.Visitor_ID = p.Visitor_ID
                WHERE p.Approval_Status = TRUE;
            """)

    async def get_cars():
        async with db_pool.acquire() as conn:
            return await conn.fetch("""
                SELECT *
                FROM Car
                ORDER BY Model
            """)

    async def approve_visitor(visitor_id):
        async with db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE Permissions
                SET Approval_Status = TRUE
                WHERE Visitor_ID = $1
            """, visitor_id)
            await conn.execute("""
                INSERT INTO log (date, time, visitor_id, car_id)
                VALUES (CURRENT_DATE, CURRENT_TIME, $1, NULL)
            """, visitor_id)

    async def log_car_approval(car_number):
        async with db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO log (date, time, visitor_id, car_id)
                VALUES (CURRENT_DATE, CURRENT_TIME, NULL, $1)
            """, car_number)

    async def request_visitor_permission(visitor_name, phone_number, purpose, house_number, badge_number):
        async with db_pool.acquire() as conn:
            full_visit_time = datetime.now()
            date_part = full_visit_time.strftime("%Y%m%d")
            time_suffix = str(int(full_visit_time.timestamp() * 1000))[-4:]
            visitor_id = int(date_part + time_suffix)
            visitor_id = visitor_id % 10000
            permission_id = await generate_unique_permission_id(conn)
            async with conn.transaction():
                await conn.execute("""
                    INSERT INTO Visitor (Visitor_id,Visitor_Name, Phone_Number, Has_Passkey, Visit_Purpose)
                    VALUES ($1, $2, $3, $4,$5)
                """, visitor_id, visitor_name, phone_number, False, purpose)

                await conn.execute("""
                    INSERT INTO Permissions (Permission_id, Issue_Time, Approval_Status, Resident_House_Number, Visitor_ID, Guard_Badge_Number)
                    VALUES ($1,CURRENT_TIMESTAMP, FALSE, $2, $3, $4)
                """, permission_id, house_number, visitor_id, badge_number)

                await conn.execute("""
                    INSERT INTO Guard_Asks_For_Permission (Guard_ID, Permission_ID, Request_Timestamp)
                    VALUES ($1, $2, CURRENT_TIMESTAMP)
                """, badge_number, permission_id)

                await conn.execute("""
                    INSERT INTO permission_asked_from_resident (permission_id, house_number)
                    VALUES ($1, $2)
                """, permission_id, house_number)

    badge = st.session_state.user_id
    st.markdown(f"## Hi, Guard {badge} — Welcome back!")

    if "guard_section" not in st.session_state:
        st.session_state.guard_section = "dashboard"

    with st.sidebar:
        st.markdown("## 📋 Dashboard")
        if st.button("🏠 Dashboard"):
            st.session_state.guard_section = "dashboard"
        if st.button("🧑‍💼 My Shifts"):
            st.session_state.guard_section = "shifts"
        if st.button("📅 Allow Visitors"):
            st.session_state.guard_section = "allow_visitors"
        if st.button("🚗 Allow Cars"):
            st.session_state.guard_section = "allow_cars"
        if st.button("🛠 Request Permission"):
            st.session_state.guard_section = "request_permission"
        st.markdown("---")
        if st.button("🔓 Logout"):
            for key in ["logged_in", "user_type", "user_id", "activity_log", "guard_section"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    section = st.session_state.guard_section

    if section == "dashboard":
        st.markdown("### Overview")
        col1, col2 = st.columns(2)
        col1.metric("Visitors Checked", 23)
        col2.metric("Cars Allowed", 14)

    elif section == "shifts":
        shift, doj = asyncio.run(get_guard_info(badge))
        st.markdown("### 🧑‍💼 My Shifts")
        st.info(f"**Shift Timing:** {shift}")
        st.info(f"**Date of Joining:** {doj.strftime('%B %d, %Y')}")

    elif section == "allow_visitors":
        st.markdown("### 📅 Allow Visitors")
        visitors = asyncio.run(get_visitorsGuard())
        search = st.text_input("Search Visitor by Name or Phone")
        for v in visitors:
            if search.lower() in v['visitor_name'].lower() or search in v['phone_number']:
                st.markdown(f"**{v['visitor_name']}** - {v['phone_number']}")
                if st.button(f"✅ Allow {v['visitor_name']}", key=v['visitor_id']):
                    asyncio.run(approve_visitor(v['visitor_id']))
                    st.success(f"{v['visitor_name']} allowed!")
                    add_log(f"Visitor {v['visitor_name']} approved by Guard {badge}")

    elif section == "allow_cars":
        st.markdown("### 🚗 Allow Cars")
        cars = asyncio.run(get_cars())
        search = st.text_input("Search Car by Reg Number or Model")
        for c in cars:
            if search.lower() in c['model'].lower() or search in c['registration_number']:
                st.markdown(f"**{c['model']}** - {c['registration_number']}")
                if st.button(f"✅ Allow {c['model']}", key=c['car_number']):
                    asyncio.run(log_car_approval(c['car_number']))
                    st.success(f"Car {c['model']} allowed!")
                    add_log(f"Car {c['model']} approved by Guard {badge}")

    elif section == "request_permission":
        st.markdown("### 🛠 Request Visitor Permission")
        visitor_name = st.text_input("Visitor Name")
        phone_number = st.text_input("Phone Number")
        purpose = st.text_input("Visit Purpose")
        house_number = st.text_input("House Number")
        st.text_input("Badge Number", value=str(badge), disabled=True)
        if st.button("📨 Request Permission"):
            asyncio.run(request_visitor_permission(visitor_name, phone_number, purpose, int(house_number), badge))
            st.success(f"Requested permission for visitor {visitor_name} to house {house_number}")
            add_log(f"Requested permission for visitor {visitor_name} to house {house_number}")

    # Activity Log (exactly like resident)
    st.markdown("---")
    st.markdown("### Activity Log")
    for log_entry in st.session_state.activity_log:
        st.markdown(f"- {log_entry}")

async def get_guards_by_shift():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT shift_timings, COUNT(*) AS count
            FROM Guard
            GROUP BY Shift_Timings
        """)
        guard_shifts = {row["shift_timings"]: row["count"] for row in rows}
        return guard_shifts

async def get_owner_count():
    async with db_pool.acquire() as conn:
        result = await conn.fetchval("""
            SELECT COUNT(*)
            FROM Resident
            WHERE Status = 'Owner'
        """)
        return result

async def get_visitors_with_passkey():
    async with db_pool.acquire() as conn:
        row = await conn.fetchval("""
            SELECT COUNT(*)
            FROM Visitor
            WHERE Has_Passkey = TRUE
        """)
        return row

async def get_permissions_in_last_x_days(days=7):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT COUNT(*) AS permission_count
            FROM Permissions
            WHERE Issue_Time >= NOW() - ($1 * INTERVAL '1 day')
        """, days)
        return row["permission_count"]

async def get_most_booked_amenity():
    async with db_pool.acquire() as conn:
        rows = await conn.fetchrow("""
            SELECT Amenity_Name, COUNT(*) AS Booking_Count 
            FROM Resident_Books_Amenity RBA 
            JOIN Amenities A ON RBA.Amenity_ID = A.Amenity_ID 
            GROUP BY Amenity_Name 
            ORDER BY Booking_Count DESC 
            LIMIT 1; 
        """)
        if rows:
            amenity_name = rows["amenity_name"]
            booking_count = rows["booking_count"]
            return {amenity_name: booking_count}
        return {}

async def get_cars_parked_by_residents():
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(""" 
            SELECT COUNT(*) AS CarsParked 
            FROM Car 
            WHERE Resident_House_Number IS NOT NULL
        """)
        return row[0] if row else 0

async def get_services_ordered():
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT COUNT(*) AS ServicesOrdered
            FROM Resident_Orders_Service
        """)
        return row

async def get_average_cost_of_services():
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT AVG(Cost) AS AverageCost
            FROM Services
        """)
        return row
    
async def get_guard_tenure_distribution():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT 
                DATE_PART('year', AGE(current_date, Date_Of_Joining)) AS Years_Of_Service,
                COUNT(*) AS Guard_Count
            FROM Guard
            GROUP BY Years_Of_Service
            ORDER BY Years_Of_Service DESC
        """)
        return rows
    
async def get_amenity_usage_trends():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT 
                a.Amenity_Name,
                rba.Booking_Date,
                COUNT(*) AS Booking_Count
            FROM Resident_Books_Amenity rba
            JOIN Amenities a ON rba.Amenity_ID = a.Amenity_ID
            WHERE rba.Booking_Date >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY a.Amenity_Name, rba.Booking_Date
            ORDER BY rba.Booking_Date DESC
        """)
        return rows
    
async def get_active_residents_count():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT COUNT(DISTINCT House_Number) AS Active_Residents
            FROM (
                SELECT House_Number FROM Resident_Books_Amenity 
                WHERE Booking_Date >= CURRENT_DATE - INTERVAL '30 days'
                UNION
                SELECT House_Number FROM Resident_Orders_Service 
                WHERE Date >= CURRENT_DATE - INTERVAL '30 days'
            ) AS ActiveRecent
        """)
        return rows

async def get_visitors_allowed_by_guards():
    async with db_pool.acquire() as conn:
        result = await conn.fetchval("""
            SELECT COUNT(DISTINCT Visitor_ID)
            FROM Permissions
            WHERE Approval_Status = TRUE
        """)
        return result

async def get_guard_permission_approvals():
    async with db_pool.acquire() as conn:
        result = await conn.fetchrow("""
            SELECT Guard_Badge_Number AS guard_id, COUNT(*) AS approvals
            FROM Permissions
            WHERE Approval_Status = TRUE
            GROUP BY Guard_Badge_Number
            ORDER BY approvals DESC
            LIMIT 1
        """)
        return result["guard_id"] if result else None

async def get_pending_approvals_count():
    async with db_pool.acquire() as conn:
        result = await conn.fetchval("""
            SELECT COUNT(*)
            FROM Permissions
            WHERE Approval_Status = FALSE
        """)
        return result

async def get_live_visitor_count_today():
    async with db_pool.acquire() as conn:
        today = datetime.today()
        result = await conn.fetchval("""
            SELECT COUNT(DISTINCT Visitor_ID)
            FROM Log
            WHERE Date = $1
        """, today)
        return result
##################
async def get_all_residents():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT *
            FROM resident;
        """)
        if rows:
            return [dict(row) for row in rows]
        else:
            return []

async def get_services_ordered_by_residents():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT R.Owner_Name, S.Service_Name, S.Cost, ROS.Delivery_Status
            FROM Resident_Orders_Service ROS
            JOIN Resident R ON ROS.House_Number = R.House_Number
            JOIN Services S ON ROS.Service_ID = S.Service_ID;
        """)
        return [dict(row) for row in rows]

async def get_residents_with_multiple_cars():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT R.Owner_Name, COUNT(C.Car_Number) AS Number_Of_Cars
            FROM Resident R
            JOIN Car C ON R.House_Number = C.Resident_House_Number
            GROUP BY R.Owner_Name
            HAVING COUNT(C.Car_Number) > 1;
        """)
        return [dict(row) for row in rows]

async def get_amenity_booking_counts_per_resident():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT R.Owner_Name, COUNT(RBA.Booking_ID) AS Total_Bookings
            FROM Resident R
            JOIN Resident_Books_Amenity RBA ON R.House_Number = RBA.House_Number
            GROUP BY R.Owner_Name
            ORDER BY Total_Bookings DESC;
        """)
        return [dict(row) for row in rows]
#######################
async def get_all_guards():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM Guard;")
        return [dict(row) for row in rows]

async def get_guards_with_invalid_passkey_checks():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT V.Visitor_Name, G.Guard_Name, GCP.Check_Timestamp
            FROM Guard_Checks_Passkey GCP
            JOIN Guard G ON GCP.Guard_ID = G.Badge_Number
            JOIN Visitor V ON GCP.Visitor_ID = V.Visitor_ID
            WHERE GCP.Passkey_Status = 'Invalid';
        """)
        return [dict(row) for row in rows]

async def get_permissions_requested_by_guard(guard_id=1001):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT P.Permission_ID, P.Issue_Time, P.Approval_Status, R.Owner_Name
            FROM Permissions P
            JOIN Guard_Asks_For_Permission GAP ON P.Permission_ID = GAP.Permission_ID
            JOIN Resident R ON P.Resident_House_Number = R.House_Number
            WHERE GAP.Guard_ID = $1;
        """, guard_id)
        return [dict(row) for row in rows]
#######################
async def get_all_amenities():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM Amenities;")
        return [dict(row) for row in rows]    
    
async def get_average_booking_per_amenity():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT a.Amenity_Name, COUNT(rba.Booking_ID) AS Total_Bookings
            FROM Amenities a
            LEFT JOIN Resident_Books_Amenity rba ON a.Amenity_ID = rba.Amenity_ID
            GROUP BY a.Amenity_Name
            ORDER BY Total_Bookings DESC;
        """)
        return [dict(row) for row in rows]

async def get_top_amenity_users():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT r.Owner_Name, COUNT(*) AS Booking_Count
            FROM Resident_Books_Amenity rba
            JOIN Resident r ON r.House_Number = rba.House_Number
            GROUP BY r.Owner_Name
            ORDER BY Booking_Count DESC
            LIMIT 5;
        """)
        return [dict(row) for row in rows]

async def get_amenity_availability_status():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT Amenity_Name, Availability_Status
            FROM Amenities;
        """)
        return [dict(row) for row in rows]    

def admin_dashboard():
    st.markdown("## 👩‍💼 Admin Dashboard")

    with st.sidebar:
        st.markdown("## 🛠 Admin Controls")
        if st.button("📊 Overview"):
            st.session_state.admin_section = "overview"
        if st.button("👥 Manage Residents"):
            st.session_state.admin_section = "manage_residents"
        if st.button("🧑‍✈️ Manage Guards"):
            st.session_state.admin_section = "manage_guards"
        if st.button("📆 Amenities"):
            st.session_state.admin_section = "amenities"
        if st.button("🔓 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    section = st.session_state.get("admin_section", "overview")

    if section == "overview":
        st.subheader("🏠 Society Overview")
    
        results = asyncio.run(asyncio.gather(
            get_owner_count(),
            get_cars_parked_by_residents(),
            get_guards_by_shift(),
            get_visitors_with_passkey(),
            get_most_booked_amenity(),
            get_visitors_allowed_by_guards(),
            get_guard_permission_approvals(),
            get_pending_approvals_count(),
            get_live_visitor_count_today()
        ))
        #
        (owner_count, cars_parked, guard_shifts, 
         passkey_visitors, top_amenity, allowed_visitors, top_guard,
         pending_approvals, live_visitor_count) = results

        # Row 1
        col1, col2, col3 = st.columns(3)
        col1.metric("🧑‍🤝‍🧑 Owner Count", owner_count or "0")
        col2.metric("🚗 Cars Parked by Residents", cars_parked or "0")
        col3.metric("🛡 Guards on Duty", sum(guard_shifts.values()) if guard_shifts else "0")

        x12, y23 = st.columns([4,20])
        num_days = x12.number_input("Show permissions in last X days", min_value=1, max_value=30, value=7)
        t = asyncio.run(get_permissions_in_last_x_days(num_days))
        y23.metric(f"📋 Permissions in Last {num_days} Days", t or "0")

        col5, col6 = st.columns(2)
        col5.metric("🛡 Guards by Shift", f"{guard_shifts.get('Day',0)} Day / {guard_shifts.get('Night',0)} Night / {guard_shifts.get('Evening',0)} Evening")
        col6.metric("✅ Visitors with Passkey", passkey_visitors or "0")

        # Row 3
        col8, col9 = st.columns(2)
        col8.metric("👮‍♂️ Visitors Allowed by Guards", allowed_visitors or "0")
        col9.metric("💪 Top Guard (Approvals)", f"Guard #{top_guard}" if top_guard else "N/A")

        # Row 4
        col10, col11 = st.columns(2)
        col10.metric("🆗 Pending Approvals", f"{pending_approvals or 0} Requests")
        col11.metric("📊 Live Visitor Count (Today)", live_visitor_count or "0")

        col12, col13 = st.columns(2)
        col12.write("🎯 Most Booked Amenity")
        col12.table(pd.DataFrame(list(top_amenity.items()), columns=['Amenity Name', 'Booking Count']))

        st.markdown("---")
        st.info("Use the dashboard to give an overall insight to the residence, use the sidebar for specifics.")

    elif section == "manage_residents":
        st.subheader("👥 Manage Residents")

        # Run all relevant resident queries asynchronously
        results = asyncio.run(asyncio.gather(
            get_all_residents(),                  # Query 2 - Owners count (but now we show all residents)
            get_services_ordered_by_residents(),  # Query 9
            get_residents_with_multiple_cars(),   # Query 12
            get_amenity_booking_counts_per_resident()  # Query 14
        ))

        all_residents, service_orders, multi_car_residents, amenity_bookings = results

        #print("===================================================")
        st.markdown("### 🏘 All Residents")
        st.dataframe(pd.DataFrame(all_residents, columns=["house_number", "owner_name", "phone_number", "move_in_date", "status"]))

        st.markdown("### 📦 Services Ordered by Residents")
        st.dataframe(pd.DataFrame(service_orders, columns=["owner_name", "service_name", "cost", "delivery_status"]))

        st.markdown("### 🚘 Residents with Multiple Cars")
        if len(multi_car_residents) == 0:
            st.write("None")
        else:
            st.dataframe(pd.DataFrame(multi_car_residents, columns=["owner_name", "number_of_cars"]))

        st.markdown("### 🏋️ Amenity Bookings by Residents")
        st.dataframe(pd.DataFrame(amenity_bookings, columns=["owner_name", "total_bookings"]))

    elif section == "manage_guards":
        st.subheader("🧑‍✈️ Manage Guards")
    
        results = asyncio.run(asyncio.gather(
            get_all_guards(),  # All guards
            get_guard_tenure_distribution(),  # Tenure
            get_guards_with_invalid_passkey_checks(),  # Invalid passkey checks
            get_permissions_requested_by_guard(101)  # Permissions requested by specific guard
        ))
    
        all_guards, tenure_data, invalid_checks, guard_permission_requests = results
    
        st.markdown("### 🛡 All Guards")
        st.dataframe(pd.DataFrame(all_guards, columns=["badge_number", "guard_name", "shift_timings", "date_of_joining", "phone_number"]))
    
        st.markdown("### 📅 Guard Tenure Distribution (Years of Service)")
        if len(tenure_data):
            df_tenure = pd.DataFrame(tenure_data, columns=["years_of_service", "guard_count"])
            st.area_chart(df_tenure.set_index("years_of_service"))
        else:
            st.write("No tenure data available.")
    
        st.markdown("### 🚫 Invalid Passkey Checks by Guards")
        if invalid_checks:
            st.dataframe(pd.DataFrame(invalid_checks, columns=["visitor_name", "guard_name", "check_timestamp"]))
        else:
            st.write("No invalid passkey checks recorded.")
    
        st.markdown("### 📝 Permissions Requested by Guard #1001")
        if guard_permission_requests:
            st.dataframe(pd.DataFrame(guard_permission_requests, columns=["permission_id", "issue_time", "approval_status", "owner_name"]))
        else:
            st.write("No permission requests by this guard.")

    elif section == "amenities":
        st.subheader("🏋️ Amenities Overview")

        results = asyncio.run(asyncio.gather(
            get_all_amenities(),
            get_amenity_usage_trends(),
            get_average_booking_per_amenity(),
            get_top_amenity_users(),
            get_amenity_availability_status()
        ))

        all_amenities, usage_trends, average_booking, top_users, availability = results

        st.markdown("### 📋 All Amenities")
        st.dataframe(pd.DataFrame(all_amenities))

        st.markdown("### 📈 Amenity Usage in Last 30 Days")
        df_trend = pd.DataFrame(usage_trends)
        if not df_trend.empty:
            df_trend.columns = ["amenity_name", "booking_date", "booking_count"]  # Rename the columns
            df_trend["booking_date"] = pd.to_datetime(df_trend["booking_date"])  # Convert to datetime
            df_pivot = df_trend.pivot_table(
                index="booking_date",
                columns="amenity_name",
                values="booking_count",
                aggfunc="sum"
            ).fillna(0)
            st.area_chart(df_pivot)
        else:
            st.write("No recent bookings.")

        coll1, coll2 = st.columns(2)
        coll1.markdown("### 📊 Average Booking Count per Amenity")
        coll1.dataframe(pd.DataFrame(average_booking, columns=["amenity_name", "total_bookings"]))

        coll2.markdown("### 👑 Top Amenity Users")
        coll2.dataframe(pd.DataFrame(top_users, columns=["owner_name", "booking_count"]))

        st.markdown("### ✅ Amenity Availability Status")
        st.dataframe(pd.DataFrame(availability, columns=["amenity_name", "availability_status"]))
        
if page == "resident" and st.session_state.logged_in:
    resident_dashboard()
    st.stop()
elif page == "guard" and st.session_state.logged_in:
    guard_dashboard()
    st.stop()
elif page == "Admin" and st.session_state.logged_in:
    admin_dashboard()
    st.stop()



# LOGIN SECTION
if not st.session_state.logged_in:
    st.title("🔐 Login to SmartGate")

    user_type = st.selectbox("Login as", ["Resident", "Guard", "Admin"])
    if user_type == "Admin":
        password = st.text_input("Enter Password", type="password")
        if st.button("Login"):
            if password != "1234":
                st.error("Incorrect password.")
            else:
                st.session_state.logged_in = True
                st.session_state.user_type = "Admin"
                st.session_state.user_id = "Admin"
                st.query_params["page"] = "Admin"
                st.rerun()
    else:
        user_id = st.text_input("Enter House Number" if user_type == "Resident" else "Enter Badge Number")
        password = st.text_input("Enter Password", type="password")

        if st.button("Login"):
            if password != "1234":
                st.error("Incorrect password.")
            elif not user_id.strip().isdigit():
                st.error("Please enter a valid numeric ID.")
            else:
                user_id = int(user_id.strip())
                if user_type == "Resident":
                    if asyncio.run(is_valid_resident(user_id)):
                        st.session_state.logged_in = True
                        st.session_state.user_type = "Resident"
                        st.session_state.user_id = user_id
                        st.query_params["page"] = "resident"
                        st.rerun()
                    else:
                        st.error("House number not found.")
                else:
                    if asyncio.run(is_valid_guard(user_id)):
                        st.session_state.logged_in = True
                        st.session_state.user_type = "Guard"
                        st.session_state.user_id = user_id
                        st.query_params["page"] = "guard"
                        st.rerun()
                    else:
                        st.error("Badge number not found.")
    st.stop()
