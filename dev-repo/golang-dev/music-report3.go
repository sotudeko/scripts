package main

import (
	"strings"
	"io/ioutil"
	"fmt"
 )

func main() {

	music_lib := "/Volumes/Users/sola/Music/iTunes/iTunes Music/"

	artists, err := ioutil.ReadDir(music_lib)
	if err != nil {
		panic(err)
	}

	for _, file := range artists {

		var artist = file.Name()
		var artistDir = music_lib + "/" + artist

		if strings.HasPrefix(artist, ".") || 
		   strings.HasPrefix(artist, "Automatically") ||
		   artist == "Compilations" ||
		   artist == "Home Videos" ||
		   artist == "Open University" ||
		   artist == "Ram Nidumolu, C.K. Prahalad, M.R. Rangaswam" ||
		   artist == "TV Shows" ||
		   artist == "Books" ||
		   artist == "Voice Memos" ||
		   artist == "Tones" ||
		   artist == "iTunes U" ||
		   artist == "Podcasts" ||
		   artist == "Movies" ||
		   artist == "Downloads" ||
		   artist == "Clayton Christensen" ||
		   artist == "Apple Music" {
			continue
		}

		artistAlbums, err := ioutil.ReadDir(artistDir)
		if err != nil {
			panic(err)
		}

		fmt.Println(artist)

		for _, album := range artistAlbums {
			var albumName = album.Name()

			if strings.HasPrefix(albumName, ".") ||
			   albumName == "www.cicana.coc" {
				continue
			}

			if album.IsDir() {
				fmt.Println("  " + albumName)
			}
		}
	}
}

