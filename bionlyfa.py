import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

# Function to search users by partial username (scraping Roblox search)
def search_users_by_username(username):
    url = f"https://www.roblox.com/search/users/results?q={username}&type=users"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            user_cards = soup.find_all('div', {'class': 'search-result-card'})
            
            if not user_cards:
                return "No users found matching that username."
            
            users = []
            for card in user_cards:
                user_name = card.find('a', {'class': 'search-result-title'})
                if user_name:
                    user_name_text = user_name.text.strip()
                    users.append(user_name_text)
            
            return users
        else:
            return f"Error: Unable to fetch results. Status code: {response.status_code}"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to search users by bio (scraping Roblox user profiles)
def search_users_by_bio(bio_query):
    url = f"https://www.roblox.com/search/users/results?q={bio_query}&type=users"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            user_cards = soup.find_all('div', {'class': 'search-result-card'})
            
            if not user_cards:
                return "No users found with that bio."
            
            users = []
            for card in user_cards:
                user_name = card.find('a', {'class': 'search-result-title'})
                bio = card.find('div', {'class': 'bio-text'})
                
                if user_name:
                    user_name_text = user_name.text.strip()
                    bio_text = bio.text.strip() if bio else "No bio"
                    if bio_text.lower() == bio_query.lower():  # Match the bio text
                        users.append((user_name_text, bio_text))
            
            return users
        else:
            return f"Error: Unable to fetch results. Status code: {response.status_code}"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to handle search by username
def handle_search_by_username():
    search_term = search_entry.get()
    if not search_term:
        messagebox.showwarning("Input Error", "Please enter a username to search for.")
        return
    
    results = search_users_by_username(search_term)
    
    result_listbox.delete(0, tk.END)
    
    if isinstance(results, list):
        for user in results:
            result_listbox.insert(tk.END, f"Username: {user}")
    else:
        result_listbox.insert(tk.END, results)

# Function to handle search by bio
def handle_search_by_bio():
    search_term = search_entry.get()
    if not search_term:
        messagebox.showwarning("Input Error", "Please enter a bio to search for.")
        return
    
    results = search_users_by_bio(search_term)
    
    result_listbox.delete(0, tk.END)
    
    if isinstance(results, list):
        for user in results:
            result_listbox.insert(tk.END, f"Username: {user[0]}, Bio: {user[1]}")
    else:
        result_listbox.insert(tk.END, results)

# Create the Tkinter window
root = tk.Tk()
root.title("Roblox Profile Searcher")
root.geometry("600x600")
root.configure(bg="#f5f5f5")

# Frame for the UI
frame = tk.Frame(root, bg="#f5f5f5")
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Label and entry for search
search_label = tk.Label(frame, text="Enter Roblox Username or Bio:", font=("Arial", 14), bg="#f5f5f5")
search_label.pack(padx=10, pady=10)

search_entry = tk.Entry(frame, width=40, font=("Arial", 12))
search_entry.pack(padx=10, pady=10)

# Buttons for searching
search_username_button = tk.Button(frame, text="Search by Username", font=("Arial", 12), bg="#4CAF50", fg="white", command=handle_search_by_username)
search_username_button.pack(padx=10, pady=10, fill="x")

search_bio_button = tk.Button(frame, text="Search by Bio", font=("Arial", 12), bg="#2196F3", fg="white", command=handle_search_by_bio)
search_bio_button.pack(padx=10, pady=10, fill="x")

# Listbox to display results
result_listbox = tk.Listbox(frame, width=70, height=15, font=("Arial", 12), bg="#f5f5f5", selectmode=tk.SINGLE)
result_listbox.pack(padx=10, pady=10, fill="both", expand=True)

# Start the Tkinter loop
root.mainloop()
