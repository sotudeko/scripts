package main

import (
	"path/filepath"
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
			var albumDir = music_lib + "/" + artist + "/" + albumName

			if strings.HasPrefix(albumName, ".") ||
			   albumName == "www.cicana.coc" {
				continue
			}

			if album.IsDir() {
				fmt.Println("  " + albumName)

				albumTracks, err := ioutil.ReadDir(albumDir)
				if err != nil {
					panic(err)
				}

				var hasMp3 = false
				var hasM4a = false
				
				for _, track := range albumTracks {
					var trackName = track.Name()
					var trackPath = albumDir + "/" + trackName
					
					if strings.HasPrefix(trackName, ".") {
						continue
					}

					if filepath.Ext(trackPath) == ".mp3" {
						hasMp3 = true	
					}

					if filepath.Ext(trackPath) == ".m4a" {
						hasM4a = true	
					}
					
					if hasMp3 && hasM4a {
						fmt.Println("    *" + track.Name())
					}
				}
			}
		}
	}
}

