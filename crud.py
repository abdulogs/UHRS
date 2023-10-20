from database import Listing, Create, Delete, Update



# Listing record
# listing = Listing(table="test", columns=["firstname", "lastname"], order={"id" : "DESC"}, condition={"id": 1}, single=True)

# for item in listing:
#     print(listing["firstname"],listing["lastname"])


# # Delete record
# Delete(table="test", condition={"id": 5})


# # Create record
Create(table="test", columns={
    "fullname": "Arsalan",
    "email": "arsalan@gmail.com"
})


# # Update record
Update(table="test", columns={
    "fullname": "Arsalan",
    "email": "arsalan@gmail.com"
}, condition={"id": 4})
