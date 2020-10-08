package main

import (
	"path/filepath"
	"strings"
	"io/ioutil"
	"fmt"
 )

func main() {

	music_lib := "/Volumes/Users/sola/Music/iTunes/iTunes Music/Compilations"

	albums, err := ioutil.ReadDir(music_lib)
	if err != nil {
		panic(err)
	}

	for _, album := range albums {

		var albumName = album.Name()
		var albumDir = music_lib + "/" + albumName

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

