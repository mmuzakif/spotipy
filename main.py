import pygame
import json
#OOP
class Song:
    def __init__(self, title, artist, path):
        self.title = title
        self.artist = artist
        self.path = path
lagu = []
with open("songs.json","r")as f:
    data = json.load(f)
for i in data:
    lagu.append(
        Song(
            i["title"],
            i["artist"],
            i["path"]
        )
    )
#bst node
class Node:
    def __init__(self, song):
        self.song = song
        self.left = None
        self.right = None
# =========================================
# BST INSERT
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
# BST SEARCH
# =========================================

def search(root, title):

    if root is None:

        return None

    # FOUND
    if title.lower() == root.song.title.lower():

        return root.song

    # GO LEFT
    elif title.lower() < root.song.title.lower():

        return search(root.left, title)

    # GO RIGHT
    else:

        return search(root.right, title)
# =========================================
# BST INORDER TRAVERSAL
# =========================================
def inorder(root):
    if root:

        inorder(root.left)

        print(
            root.song.title,
            "-",
            root.song.artist
        )

        inorder(root.right)
# =========================================
# BUILD BST
# =========================================
root = None

for song in lagu:

    root = insert(root, song)

# =========================================
# GRAPH RECOMMENDATION SYSTEM
# =========================================
graph = {

    "ride": [
        "glimpse of us",
        "lose",
        "snooze"
    ],

    "akhir tak bahagia": [
        "secukupnya",
        "rumah ke rumah",
        "traitor"
    ],

    "leave the door open": [
        "earned it",
        "get you",
        "snooze"
    ],

    "secukupnya": [
        "rumah ke rumah",
        "akhir tak bahagia",
        "about you"
    ],

    "glimpse of us": [
        "get you",
        "lose",
        "about you"
    ],

    "get you": [
        "japanase denim",
        "earned it",
        "snooze"
    ],

    "about you": [
        "heavenly",
        "glimpse of us",
        "ride"
    ],

    "cruel summer": [
        "traitor",
        "feather",
        "lose"
    ],

    "traitor": [
        "cruel summer",
        "akhir tak bahagia",
        "feather"
    ],

    "snooze": [
        "get you",
        "earned it",
        "lose"
    ],

    "rumah ke rumah": [
        "secukupnya",
        "akhir tak bahagia",
        "about you"
    ],

    "earned it": [
        "get you",
        "leave the door open",
        "snooze"
    ],

    "dady issues": [
        "heavenly",
        "about you",
        "ride"
    ],

    "heavenly": [
        "about you",
        "dady issues",
        "glimpse of us"
    ],

    "feather": [
        "cruel summer",
        "traitor",
        "lose"
    ],

    "pasilyo": [
        "secukupnya",
        "rumah ke rumah",
        "akhir tak bahagia"
    ],

    "japanase denim": [
        "get you",
        "snooze",
        "earned it"
    ],

    "lose": [
        "glimpse of us",
        "ride",
        "snooze"
    ]
}
history = []
# =========================================
# SHOW RECOMMENDATION
# =========================================
def show_recommendation(song_title):
    print("\n===== RECOMMENDATION =====")

    if song_title in graph:

        for rekomendasi in graph[song_title]:

            for song in lagu:

                if song.title == rekomendasi:

                    print(
                        "-",
                        song.title,
                        "-",
                        song.artist
                    )

    else:

        print("No recommendation found")
#untuk putar lagu
def func_lagu(masukan,list_lagu):
   pygame.init()
   pygame.mixer.init()
   song = list_lagu[masukan - 1]
   add_history(current_user,song)
   count_thesong(current_user,song)
   print("🔊.......................")
   print("----------NOW PLAYING------------")
   print(song.title)
   print(song.artist)
   show_recommendation(song.title)
   pygame.mixer.music.load(song.path)
   pygame.mixer.music.play()
   input("Press Enter to stop the music...........")
   pygame.mixer.music.stop()

# =========================================
# SHOW HISTORY
# =========================================

def show_history(current_user):
    with open ("users.json","r") as f:
        u = json.load(f)

    print("\n===== PLAYBACK HISTORY =====")
    history = u[current_user]["history"]

    if len(history) == 0:

        print("No history yet")
        return

    for song in reversed(history):

        print(
            song["title"],
            "-",
            song["artist"]
        )
# =========================================
# SHOW QUEUE
# =========================================

def show_queue(current_user):

    print("\n===== SONG QUEUE =====")
    with open("users.json","r") as f:
        u = json.load(f)
    if len(u[current_user]["queue"]) == 0:
        print("Queue kosong")
        return

    for index, song in enumerate(u[current_user]["queue"]):

        print(
            index + 1,
            ".",
            song["title"],
            "-",
            song["artist"]
        )
# =========================================
# PLAY NEXT QUEUE
# =========================================

def play_next_queue(current_user):
    queue = []
    with open("users.json","r")as f:
        u = json.load(f)

    if len(u[current_user]["queue"]) == 0:

        print("Queue kosong")
        return


    # FIFO
    next_song = u[current_user]["queue"].pop(0)
    u[current_user]["history"].append({
        "title":next_song["title"],
        "artist":next_song["artist"]
    })
    with open("users.json","w")as f:
        json.dump(u,f,indent=4)

    #u[cu].append(next_song)
    
    for index,song in enumerate(lagu):
        if next_song["title"] == song.title:
            index_lagu = index + 1
    func_lagu(index_lagu,lagu)
#list of available song
def song_list(lagu):
      with open ("users.json","r") as f:
          u = json.load(f)
      for index, song in enumerate(lagu):
        print(index + 1,".",song.title,"-",song.artist)
      pilih_lagu = input("pilih lagu:")
      pilih_lagu1 = int(pilih_lagu)
      song = lagu[pilih_lagu1 - 1]
      """     
      u[current_user]["history"].append(
          {
              "title":song.title,
              "artist":song.artist
          }
      )
      with open("users.json","w")as f:
          json.dump(u,f,indent=4)
     """
      func_lagu(pilih_lagu1,lagu)
#login
def login(login):
  while True:
    with open("users.json","r") as f:
        u = json.load(f)
        if login in u:
          while True:
            pw = input("masukan password:")
            if u[login]["password"] == pw:
                print("login berhasil!!!")
                return login
            elif u[login]["password"] != pw:
                print("password salah")
        else:
           print("pastikan username pernah terdaftar")
#sign up
def sign_up():
    username = input("masukan username baru:")
    pw = input("masukan password:")
    with open("users.json","r") as f:
        u = json.load(f)
    u[username] = {
            "password":pw,
            "history": [],
            "queue": [],
            "playcount":{},
            "playlist":[]
    }
    with open("users.json","w") as f:
        json.dump(u,f, indent = 4)
    print("sign up berhasil!!!")
    print("silahkan login")
    print("usename baru =",username)
    return login(username)

#tambah queue
def tambah_queue(current_user):
    for index, song in enumerate(lagu):

        print(index + 1, ".", song.title)

    nomor = int(input("Pilih lagu untuk queue: "))

    selected_song = lagu[nomor - 1]
    with open("users.json","r") as f:
        u = json.load(f)
    u[current_user]["queue"].append({
        "title":selected_song.title,
        "artist":selected_song.artist
    })
    with open("users.json","w") as f:
        json.dump(u,f,indent=4)

    print(selected_song.title, "ditambahkan ke queue")
#hapus history
def hapus_history(current_user):
    with open("users.json","r")as f:
        u = json.load(f)
    u[current_user]["history"] = []
    with open("users.json","w")as f:
        json.dump(u,f,indent=4)
#tambah history
def add_history(current_user,song_object):
    with open ("users.json","r")as f:
        u = json.load(f)
    for i in lagu:
        if i.title == song_object.title:
            u[current_user]["history"].append({
                "title":song_object.title,
                "artist":song_object.artist
            }
            )
    with open("users.json","w")as f:
        json.dump(u,f,indent=4)
#hitung top lagu(most played)
def count_thesong(current_user,song_object):
    with open("users.json","r")as f:
        u = json.load(f)
    if song_object.title not in u[current_user]["playcount"]:
        u[current_user]["playcount"][song_object.title] = 1
    elif song_object.title in u[current_user]["playcount"]:
        u[current_user]["playcount"][song_object.title] += 1
    with open("users.json", "w") as f:
        json.dump(u, f, indent=4)
#mengurutkan lagu yang paling banyak di mainkan
def sorting_topplay(current_user):
    with open("users.json","r")as f:
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
               temp_list[j], temp_list[j+1] = temp_list[j+1], temp_list[j]
    print("======= your top song ==========")
    print("===========Played==============")
    for i in range(n):
     print(
        i + 1,
        ".",
        temp_list[i][0],
        "- Played",
        temp_list[i][1],
        "times"
    )
#tambah lagu ke dalam program(untuk admin)  
def admin_song():
    global root 
    masukan = input("masukan judul lagu:")
    masukan2 = input("nama artist:") 
    with open ("songs.json","r")as f:
        u = json.load(f)
    u.append(
        {
            "title":masukan,
            "artist":masukan2,
            "path":"song/" + masukan + ".mp3" 
        }
    )
    with open("songs.json","w")as f:
        json.dump(u,f,indent=4)
    lagu.append(
        Song(
            masukan,
            masukan2,
            "song/" + masukan + ".mp3" 

        )

    )
    root = insert(root,insert)

#buat playlist
def made_playlist(current_user):
    with open("users.json","r")as f:
        u = json.load(f)
    masukan = input("enter the name of the playlist:")
    nama_lagu = input("masukan nama lagu:")
    for song in lagu:
        if nama_lagu == song.title:
            nama_lagu = song
    if masukan not in u[current_user]["playlist"]:
        u[current_user]["playlist"][masukan] = []
    u[current_user]["playlist"][masukan].append(
        {
            "title":nama_lagu.title,
            "artist":nama_lagu.artist
        }
    )
    with open("users.json","w")as f:
        json.dump(u,f,indent=4)
    print("====playlist sudah di buat==========")
#lihat playlist
def see_playlist(current_user):
    with open("users.json","r")as f:
        u = json.load(f)
    playlist = u[current_user]["playlist"]
    for index, playlistname in enumerate (playlist):
        print(index + 1,
              ".",
              playlistname)
    pilih_playlist = input("chose playlist name:")
    for index,song in enumerate(u[current_user]["playlist"][pilih_playlist]):   
            print(index + 1,
                ".",
                song["title"],
                "-",
                song["artist"]
            )
    pilih_lagu = input("enter the name of the song from playlist:")
    for index,song in enumerate(lagu):
        if pilih_lagu == song.title:
            index +=1
            break
    song_obj = index
    func_lagu(song_obj,lagu)

#tampilah menu utama (home)
def menu_utama():
 while True:
    sorting_topplay(current_user)
    print("Welcome To Spotify")
    print("================================")
    print("1.show list of songs")
    print("2.lihat history lagu")
    print("3.cari lagu")
    print("4.tambah lagu ke queue")
    print("5.lihat queue")
    print("6.play next queue")
    print("7.show song A-Z")
    print("8.hapus history lagu:")
    print("9.admin section")
    print("10.make playlist:")
    print("11.see playlist")
    print("12.stop")
    pilih = input("pilih menu:")
    if pilih ==  "1":
        song_list(lagu)      
    # =====================================
    # SHOW HISTORY
    # =====================================
    elif pilih == "2":
            show_history(current_user)
    # =====================================
    # BST SEARCH
    # =====================================
    elif pilih  == "3":

            keyword = input("\nInput song title: ")
            result = search(root, keyword)
            if result:
                for index,song in enumerate(lagu):
                 if song.title == result.title:
                    index_lagu  = index + 1
                    func_lagu(index_lagu,lagu)  
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
            print("admin section is limited to just the develloper")
            print("this fiture allow you to add song,delete user and change the password user")
            print("plis enter the password to access this section")
            masukan1 = input("masukan password:")
            if masukan1 == "12345":
                print("welcome!!!")
                break
            elif masukan1 != "12345":
                print("========PASSWORD SALAH==========")
                i += 1
         if i < 5:
             while True:
                 print("======welcome admin!!!!=========")
                 print("1.add song")
                 print("2.see user(coming soon)")
                 print("3.stop")
                 pilih = input("pilih menu:")
                 if pilih ==  "1":
                     print("plis note that you mush have song already in the file songs.json,if not it would cuase error")
                     pilih2 = input("countinue?(y/n):")
                     if pilih2 == "y":
                         admin_song()
                     elif pilih2 == "n":
                         print("bye")
                 elif pilih == "2":
                     print("coming soon")
                 elif pilih == "3":
                     print("bye")  
                     break
         elif i >= 5:
             print("=====Youu Not The Admin========")
             print("\n")
    elif pilih == "10":
        made_playlist(current_user)
    elif pilih == "11":
        see_playlist(current_user)
    elif pilih == "12":
        print("========Program Ended===============")
        break 

#awalan
print("1.Login")
print("2.sign up")
pilih1 = input("pilih menu:")
if pilih1 == "1":
   masukan_login = input("masukan username:")
   current_user = login(masukan_login)
   menu_utama()
elif pilih1 == "2":
    current_user = sign_up()
    menu_utama()
"""
penjelasan singkat:
menu 1:ketika menu satu dipanggil,maka akan pergi ke fungsi list_lagu untuk melihat lagu,habis tu
       setelah ditanya mau lagu apa,akan pergi ke fungsi func_lagu disana akan putar lagu dan memanggil
       fungsi yang lain untuk simpan ke history
menu 2:ketika menu 2 dipanggil,maka akan pergi ke fungs show_history untuk lihat fungsi,udh itu aja
menu 3:ketika menu 3 dipanggil,makan dia akan cari lagu,gk tau yang ini ai soalnya yang buat
menu 4:ketika menu 4 dpanggil,,maka akan pergi ke fungsi tambah queue,disana lagu ditambahkan
menu 5:ketika menu 5 dipanggil,maka akan pergi ke fungsi yang tugasnya untuk lihat queue
menu 6:ketika menu 6 dipanggil,maka akan pergi ke fungsi next_queue disni diproses segala macam,
       terus habis tu pergi ke fungsi func_lagu untu mutar lagunya ntk disana panggil fungsi yang untuk
       tambah history karena kan mutar lagu,dan pas masih di fungsi next queue nya,otomatis ngehapus queue
       yang lagi mau diputar
menu 7:ini juga gk  ngerti ai yang buat
menu 8 = nantik dia manggil fungsi untuk hapus hitory(hapus semuanya)
menu 9 = besok ya
menu 10 = 
menu 11 = 
menu 12 =

"""
