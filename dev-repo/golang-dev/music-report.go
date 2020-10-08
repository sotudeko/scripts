package main

import (
	"strings"
	"io/ioutil"
	"fmt"
 )

func main() {

	music_lib := "/Volumes/Users/sola/Music/iTunes/iTunes Music"
	//music_lib := "/Users/sotudeko/Downloads"

	artists, err := ioutil.ReadDir(music_lib)

	if err != nil {
		panic(err)
	}

	fmt.Println("[")

	for _, file := range artists {

		var artist = file.Name()
		var artistDir = "/Volumes/Users/sola/Music/iTunes/iTunes Music/" + artist

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
			// fmt.Println("skipping " + artist)
			continue
		}

		artistAlbums, err := ioutil.ReadDir(artistDir)

		if err != nil {
			panic(err)
		}

		fmt.Println("{\"artist\": \"" + artist + "\",")
		fmt.Println(" \"albums\": [")

		for _, album := range artistAlbums {
			var albumName = album.Name()

			if strings.HasPrefix(albumName, ".") ||
			   albumName == "www.cicana.coc" {
				//fmt.Println("skipping " + artist)
				continue
			}

			if album.IsDir() {
				fmt.Println("  {\"title\":" + "\"" + albumName + "\"},")
			}
		}

		fmt.Println(" ]")
		fmt.Println("},")

	}

	fmt.Println("]")

}

// [
//     {
//     "artist": "Chico Freeman & Brainstorm",
//     "albums": [
//         {
//             "title": "Sweet Explosion"
//         }
//     ]
//     },

//     {
//     "artist": "Chris Rock",
//     "albums": [
//         {
//             "title": "Bigger and Blackern"
//         },
//         {
//             "title": "Born Suspect"
//         }
//     ]
//     }
    
    
// ]

