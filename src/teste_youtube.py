from ytmusicapi import YTMusic

ytmusic = YTMusic()

resultados = ytmusic.search("Eminem Lose Yourself", filter="songs", limit=5)

for musica in resultados:
    print(musica['title'])
    print(musica['artists'][0]['name'])
    print(musica['videoId'])
    print("-------------------")