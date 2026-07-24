def login(user_id):
    # Bad practice: string formatting in SQL execute
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

# Bad practice: eval usage
user_input = "os.system('rm -rf /')"
eval(user_input)

# Bad practice: hardcoded secret
api_secret = "AKIAIOSFODNN7EXAMPLE"
