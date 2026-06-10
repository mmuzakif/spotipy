import pygame
import json

# =========================================
# OOP - SONG CLASS
# =========================================
class Song:
    def __init__(self, title, artist, path):
        self.title = title
        self.artist = artist
        self.path = path


# =========================================
# LINKED LIST - HISTORY
# =========================================
class HistoryNode:
    def __init__(self, song):
        self.song = song
        self.next = None


class HistoryLinkedList:
    def __init__(self):
        self.head = None

    def append(self, song):
        new_node = HistoryNode(song)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def show(self):
        current = self.head
        while current:
            print(current.song.title)
            current = current.next


# =========================================
# BST - NODE
# =========================================
class Node:
    def __init__(self, song):
        self.song = song
        self.left = None
        self.right = None


# =========================================
# BST - INSERT
# =========================================
def insert(root, song):
    if root is None:
        return Node(song)
    if song.title.lower() < root.song.title.lower():
        root.left = insert(root.left, song)
    else:
        root.right = insert(root.right, song)
    return root


# =========================================
# BST - SEARCH
# =========================================
def search(root, title):
    if root is None:
        return None
    if title.lower() == root.song.title.lower():
        return root.song
    elif title.lower() < root.song.title.lower():
        return search(root.left, title)
    else:
        return search(root.right, title)


# =========================================
# BST - INORDER TRAVERSAL
# =========================================
def inorder(root):
    if root:
        inorder(root.left)
        print(root.song.title, "-", root.song.artist)
        inorder(root.right)


# =========================================
# LOAD SONGS FROM JSON
# =========================================
lagu = []
try:
    with open("songs.json", "r") as f:
        data = json.load(f)
    for i in data:
        lagu.append(Song(i["title"], i["artist"], i["path"]))
except FileNotFoundError:
    print("[ERROR] songs.json tidak ditemukan.")
except json.JSONDecodeError:
    print("[ERROR] Format songs.json tidak valid.")


# =========================================
# BUILD BST
# =========================================
root = None
for song in lagu:
    root = insert(root, song)

history_linked = HistoryLinkedList()
history = []


# =========================================
# GRAPH - RECOMMENDATION SYSTEM
# =========================================
graph = {
    "ride":               ["glimpse of us", "lose", "snooze"],
    "akhir tak bahagia":  ["secukupnya", "rumah ke rumah", "traitor"],
    "leave the door open":["earned it", "get you", "snooze"],
    "secukupnya":         ["rumah ke rumah", "akhir tak bahagia", "about you"],
    "glimpse of us":      ["get you", "lose", "about you"],
    "get you":            ["japanase denim", "earned it", "snooze"],
    "about you":          ["heavenly", "glimpse of us", "ride"],
    "cruel summer":       ["traitor", "feather", "lose"],
    "traitor":            ["cruel summer", "akhir tak bahagia", "feather"],
    "snooze":             ["get you", "earned it", "lose"],
    "rumah ke rumah":     ["secukupnya", "akhir tak bahagia", "about you"],
    "earned it":          ["get you", "leave the door open", "snooze"],
    "dady issues":        ["heavenly", "about you", "ride"],
    "heavenly":           ["about you", "dady issues", "glimpse of us"],
    "feather":            ["cruel summer", "traitor", "lose"],
    "pasilyo":            ["secukupnya", "rumah ke rumah", "akhir tak bahagia"],
    "japanase denim":     ["get you", "snooze", "earned it"],
    "lose":               ["glimpse of us", "ride", "snooze"],
}


# =========================================
# SHOW RECOMMENDATION
# =========================================
def show_recommendation(song_title):
    print("\n===== RECOMMENDATION =====")
    if song_title in graph:
        for rekomendasi in graph[song_title]:
            for song in lagu:
                if song.title == rekomendasi:
                    print("-", song.title, "-", song.artist)
    else:
        print("No recommendation found")


# =========================================
# PLAY SONG
# =========================================
def func_lagu(masukan, list_lagu):
    try:
        pygame.init()
        pygame.mixer.init()
        song = list_lagu[masukan - 1]
        add_history(current_user, song)
        count_thesong(current_user, song)
        print("🔊.......................")
        print("----------NOW PLAYING------------")
        print(song.title)
        print(song.artist)
        show_recommendation(song.title)
        pygame.mixer.music.load(song.path)
        pygame.mixer.music.play()
        input("Press Enter to stop the music...........")
        pygame.mixer.music.stop()
    except pygame.error as e:
        print(f"[ERROR] Gagal memutar lagu: {e}")
    except IndexError:
        print("[ERROR] Nomor lagu tidak valid.")


# =========================================
# SHOW HISTORY
# =========================================
def show_history(current_user):
    try:
        with open("users.json", "r") as f:
            u = json.load(f)
        print("\n===== PLAYBACK HISTORY =====")
        history = u[current_user]["history"]
        if len(history) == 0:
            print("No history yet")
            return
        for song in reversed(history):
            print(song["title"], "-", song["artist"])
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")
    except KeyError:
        print("[ERROR] Data user tidak ditemukan.")


# =========================================
# SHOW QUEUE
# =========================================
def show_queue(current_user):
    try:
        with open("users.json", "r") as f:
            u = json.load(f)
        print("\n===== SONG QUEUE =====")
        if len(u[current_user]["queue"]) == 0:
            print("Queue kosong")
            return
        for index, song in enumerate(u[current_user]["queue"]):
            print(index + 1, ".", song["title"], "-", song["artist"])
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")
    except KeyError:
        print("[ERROR] Data user tidak ditemukan.")


# =========================================
# PLAY NEXT QUEUE
# =========================================
def play_next_queue(current_user):
    try:
        with open("users.json", "r") as f:
            u = json.load(f)
        if len(u[current_user]["queue"]) == 0:
            print("Queue kosong")
            return
        next_song = u[current_user]["queue"].pop(0)
        u[current_user]["history"].append({
            "title": next_song["title"],
            "artist": next_song["artist"]
        })
        with open("users.json", "w") as f:
            json.dump(u, f, indent=4)
        index_lagu = None
        for index, song in enumerate(lagu):
            if next_song["title"] == song.title:
                index_lagu = index + 1
                break
        if index_lagu is not None:
            func_lagu(index_lagu, lagu)
        else:
            print("[ERROR] Lagu dari queue tidak ditemukan di daftar lagu.")
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")
    except KeyError:
        print("[ERROR] Data user tidak ditemukan.")


# =========================================
# SONG LIST (DISPLAY & PICK)
# =========================================
def song_list(lagu):
    try:
        for index, song in enumerate(lagu):
            print(index + 1, ".", song.title, "-", song.artist)
        pilih_lagu = int(input("pilih lagu: "))
        func_lagu(pilih_lagu, lagu)
    except ValueError:
        print("[ERROR] Masukan harus berupa angka.")
    except IndexError:
        print("[ERROR] Nomor lagu tidak valid.")


# =========================================
# LOGIN
# =========================================
def login(username):
    while True:
        try:
            with open("users.json", "r") as f:
                u = json.load(f)
            if username in u:
                while True:
                    pw = input("masukan password: ")
                    if u[username]["password"] == pw:
                        print("login berhasil!!!")
                        return username
                    else:
                        print("password salah")
            else:
                print("pastikan username pernah terdaftar")
                return None
        except FileNotFoundError:
            print("[ERROR] users.json tidak ditemukan.")
            return None
        except json.JSONDecodeError:
            print("[ERROR] Format users.json tidak valid.")
            return None


# =========================================
# SIGN UP
# =========================================
def sign_up():
    try:
        username = input("masukan username baru: ")
        pw = input("masukan password: ")
        with open("users.json", "r") as f:
            u = json.load(f)
        u[username] = {
            "password": pw,
            "history": [],
            "queue": [],
            "playcount": {},
            "playlist": {}
        }
        with open("users.json", "w") as f:
            json.dump(u, f, indent=4)
        print("sign up berhasil!!!")
        print("silahkan login")
        print("username baru =", username)
        return login(username)
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")
    except json.JSONDecodeError:
        print("[ERROR] Format users.json tidak valid.")


# =========================================
# TAMBAH QUEUE
# =========================================
def tambah_queue(current_user):
    try:
        for index, song in enumerate(lagu):
            print(index + 1, ".", song.title)
        nomor = int(input("Pilih lagu untuk queue: "))
        selected_song = lagu[nomor - 1]
        with open("users.json", "r") as f:
            u = json.load(f)
        u[current_user]["queue"].append({
            "title": selected_song.title,
            "artist": selected_song.artist
        })
        with open("users.json", "w") as f:
            json.dump(u, f, indent=4)
        print(selected_song.title, "ditambahkan ke queue")
    except ValueError:
        print("[ERROR] Masukan harus berupa angka.")
    except IndexError:
        print("[ERROR] Nomor lagu tidak valid.")
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")


# =========================================
# HAPUS HISTORY
# =========================================
def hapus_history(current_user):
    global history_linked
    try:
        with open("users.json", "r") as f:
            u = json.load(f)
        u[current_user]["history"] = []
        with open("users.json", "w") as f:
            json.dump(u, f, indent=4)
        history_linked.head = None
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")
    except KeyError:
        print("[ERROR] Data user tidak ditemukan.")


# =========================================
# ADD HISTORY
# =========================================
def add_history(current_user, song_object):
    try:
        with open("users.json", "r") as f:
            u = json.load(f)
        history_linked.append(song_object)
        for i in lagu:
            if i.title == song_object.title:
                u[current_user]["history"].append({
                    "title": song_object.title,
                    "artist": song_object.artist
                })
        with open("users.json", "w") as f:
            json.dump(u, f, indent=4)
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")
    except KeyError:
        print("[ERROR] Data user tidak ditemukan.")


# =========================================
# COUNT PLAY (MOST PLAYED)
# =========================================
def count_thesong(current_user, song_object):
    try:
        with open("users.json", "r") as f:
            u = json.load(f)
        if song_object.title not in u[current_user]["playcount"]:
            u[current_user]["playcount"][song_object.title] = 1
        else:
            u[current_user]["playcount"][song_object.title] += 1
        with open("users.json", "w") as f:
            json.dump(u, f, indent=4)
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")
    except KeyError:
        print("[ERROR] Data user tidak ditemukan.")


# =========================================
# SORTING TOP PLAYED (BUBBLE SORT)
# =========================================
def sorting_topplay(current_user):
    try:
        with open("users.json", "r") as f:
            u = json.load(f)
        temp_list = list(u[current_user]["playcount"].items())
        n = len(temp_list)
        if n == 0:
            print("======= your top song ==========")
            print("=======Played============")
            print("belum ada lagu")
            return
        for i in range(n):
            for j in range(n - 1):
                if temp_list[j][1] < temp_list[j + 1][1]:
                    temp_list[j], temp_list[j + 1] = temp_list[j + 1], temp_list[j]
        print("======= your top song ==========")
        print("===========Played==============")
        for i in range(n):
            print(i + 1, ".", temp_list[i][0], "- Played", temp_list[i][1], "times")
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")
    except KeyError:
        print("[ERROR] Data user tidak ditemukan.")


# =========================================
# ADMIN - ADD SONG
# =========================================
def admin_song():
    global root
    try:
        masukan = input("masukan judul lagu: ")
        masukan2 = input("nama artist: ")
        with open("songs.json", "r") as f:
            u = json.load(f)
        u.append({
            "title": masukan,
            "artist": masukan2,
            "path": "song/" + masukan + ".mp3"
        })
        with open("songs.json", "w") as f:
            json.dump(u, f, indent=4)
        lagu.append(Song(masukan, masukan2, "song/" + masukan + ".mp3"))
        root = insert(root, lagu[-1])
        print("Lagu berhasil ditambahkan.")
    except FileNotFoundError:
        print("[ERROR] songs.json tidak ditemukan.")
    except json.JSONDecodeError:
        print("[ERROR] Format songs.json tidak valid.")


# =========================================
# BUAT PLAYLIST
# =========================================
def made_playlist(current_user):
    try:
        with open("users.json", "r") as f:
            u = json.load(f)
        masukan = input("enter the name of the playlist: ")
        nama_lagu = input("masukan nama lagu: ")
        for song in lagu:
            if nama_lagu == song.title:
                nama_lagu = song
                break
        if masukan not in u[current_user]["playlist"]:
            u[current_user]["playlist"][masukan] = []
        u[current_user]["playlist"][masukan].append({
            "title": nama_lagu.title,
            "artist": nama_lagu.artist
        })
        with open("users.json", "w") as f:
            json.dump(u, f, indent=4)
        print("====playlist sudah di buat==========")
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")
    except AttributeError:
        print("[ERROR] Lagu tidak ditemukan, pastikan nama lagu benar.")
    except KeyError:
        print("[ERROR] Data user tidak ditemukan.")


# =========================================
# LIHAT PLAYLIST
# =========================================
def see_playlist(current_user):
    try:
        with open("users.json", "r") as f:
            u = json.load(f)
        playlist = u[current_user]["playlist"]
        for index, playlistname in enumerate(playlist):
            print(index + 1, ".", playlistname)
        pilih_playlist = input("chose playlist name: ")
        for index, song in enumerate(u[current_user]["playlist"][pilih_playlist]):
            print(index + 1, ".", song["title"], "-", song["artist"])
        pilih_lagu = input("enter the name of the song from playlist: ")
        index_lagu = None
        for index, song in enumerate(lagu):
            if pilih_lagu == song.title:
                index_lagu = index + 1
                break
        if index_lagu is not None:
            func_lagu(index_lagu, lagu)
        else:
            print("[ERROR] Lagu tidak ditemukan.")
    except FileNotFoundError:
        print("[ERROR] users.json tidak ditemukan.")
    except KeyError:
        print("[ERROR] Playlist atau data user tidak ditemukan.")


# =========================================
# MENU UTAMA
# =========================================
def menu_utama():
    while True:
        sorting_topplay(current_user)
        print("Welcome To Spotify")
        print("================================")
        print("1.  show list of songs")
        print("2.  lihat history lagu")
        print("3.  cari lagu")
        print("4.  tambah lagu ke queue")
        print("5.  lihat queue")
        print("6.  play next queue")
        print("7.  show song A-Z")
        print("8.  hapus history lagu")
        print("9.  admin section")
        print("10. make playlist")
        print("11. see playlist")
        print("12. stop")
        pilih = input("pilih menu: ")

        if pilih == "1":
            song_list(lagu)

        elif pilih == "2":
            show_history(current_user)

        elif pilih == "3":
            keyword = input("\nInput song title: ")
            result = search(root, keyword)
            if result:
                for index, song in enumerate(lagu):
                    if song.title == result.title:
                        func_lagu(index + 1, lagu)
            else:
                print("\nSong not found")

        elif pilih == "4":
            tambah_queue(current_user)

        elif pilih == "5":
            show_queue(current_user)

        elif pilih == "6":
            play_next_queue(current_user)

        elif pilih == "7":
            print("\n===== SONGS A-Z =====")
            inorder(root)

        elif pilih == "8":
            hapus_history(current_user)

        elif pilih == "9":
            i = 0
            while i < 5:
                print("admin section is limited to just the developer")
                print("this feature allows you to add song, delete user, and change user password")
                masukan1 = input("masukan password: ")
                if masukan1 == "12345":
                    print("welcome!!!")
                    break
                else:
                    print("========PASSWORD SALAH==========")
                    i += 1
            if i < 5:
                while True:
                    print("======welcome admin!!!!=========")
                    print("1. add song")
                    print("2. see user (coming soon)")
                    print("3. stop")
                    pilih_admin = input("pilih menu: ")
                    if pilih_admin == "1":
                        print("note: pastikan file mp3 sudah ada di folder songs/")
                        pilih2 = input("continue? (y/n): ")
                        if pilih2 == "y":
                            admin_song()
                        elif pilih2 == "n":
                            print("bye")
                    elif pilih_admin == "2":
                        print("coming soon")